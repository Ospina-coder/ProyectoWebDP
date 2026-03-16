from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Autor
from .forms import AutorForm
from reportes.views import registrar_actividad


def lista_autores(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    autores = Autor.objects.all()
    return render(request, "autores/lista.html", {"autores": autores})


def crear_autor(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = form.save()

            registrar_actividad(
                request.user,
                "CREAR",
                "Autor",
                f"Se creó el autor {autor.nombre} con cédula {autor.cedula}",
            )
            return redirect("lista_autores")
    else:
        form = AutorForm()

    return render(request, "autores/form.html", {"form": form, "titulo": "Crear autor"})


def editar_autor(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    autor = get_object_or_404(Autor, id=id)

    if request.method == "POST":
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            autor = form.save()

            registrar_actividad(
                request.user,
                "EDITAR",
                "Autor",
                f"Se editó el autor {autor.nombre} con cédula {autor.cedula}",
            )
            return redirect("lista_autores")
    else:
        form = AutorForm(instance=autor)

    return render(
        request, "autores/form.html", {"form": form, "titulo": "Editar autor"}
    )


def eliminar_autor(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    autor = get_object_or_404(Autor, id=id)

    if request.method == "POST":
        nombre_autor = autor.nombre
        cedula_autor = autor.cedula

        registrar_actividad(
            request.user,
            "ELIMINAR",
            "Autor",
            f"Se eliminó el autor {nombre_autor} con cédula {cedula_autor}",
        )
        autor.delete()
        return redirect("lista_autores")

    return render(request, "autores/eliminar.html", {"autor": autor})
