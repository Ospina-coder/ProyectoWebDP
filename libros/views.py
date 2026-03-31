from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from .forms import LibroForm
from django.http import HttpResponseForbidden
from reportes.views import registrar_actividad
from .services import obtener_datos_libro_por_isbn


def lista_libros(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    libros = Libro.objects.select_related("autor").all()
    return render(request, "libros/lista.html", {"libros": libros})


def crear_libro(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)

            datos_api = obtener_datos_libro_por_isbn(libro.isbn)
            if datos_api:
                libro.portada_url = datos_api.get("portada_url")
                libro.titulo_api = datos_api.get("titulo_api")
                libro.editorial_api = datos_api.get("editorial_api")

            libro.save()

            registrar_actividad(
                request.user,
                "CREAR",
                "Libro",
                f"Se creó el libro {libro.titulo} con ISBN {libro.isbn}",
            )
        return redirect("lista_libros")
    else:
        form = LibroForm()

    return render(request, "libros/form.html", {"form": form, "titulo": "Crear libro"})


def editar_libro(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    libro = get_object_or_404(Libro, id=id)

    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            libro = form.save(commit=False)

            datos_api = obtener_datos_libro_por_isbn(libro.isbn)
            if datos_api:
                libro.portada_url = datos_api.get("portada_url")
                libro.titulo_api = datos_api.get("titulo_api")
                libro.editorial_api = datos_api.get("editorial_api")

            libro.save()

            registrar_actividad(
                request.user,
                "EDITAR",
                "Libro",
                f"Se editó el libro {libro.titulo} con ISBN {libro.isbn}",
            )

        return redirect("lista_libros")
    else:
        form = LibroForm(instance=libro)

    return render(request, "libros/form.html", {"form": form, "titulo": "Editar libro"})


def eliminar_libro(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    libro = get_object_or_404(Libro, id=id)

    if request.method == "POST":

        titulo_libro = libro.titulo
        isbn_libro = libro.isbn

        registrar_actividad(
            request.user,
            "ELIMINAR",
            "Libro",
            f"Se eliminó el libro {titulo_libro} con ISBN {isbn_libro}",
        )
        libro.delete()
        return redirect("lista_libros")

    return render(request, "libros/eliminar.html", {"libro": libro})
