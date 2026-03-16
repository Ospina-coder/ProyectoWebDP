from django.shortcuts import get_object_or_404, render, redirect
from autores.models import Autor
from .models import RegistroActividad
from django.http import HttpResponseForbidden


def registrar_actividad(usuario, accion, entidad, descripcion):
    RegistroActividad.objects.create(
        usuario=usuario, accion=accion, entidad=entidad, descripcion=descripcion
    )


def eliminar_registro_actividad(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    registro = get_object_or_404(RegistroActividad, id=id)

    if request.method == "POST":
        registro.delete()
        return redirect("historial_actividad")

    return render(request, "reportes/eliminar_registro.html", {"registro": registro})


def historial_actividad(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    registros = RegistroActividad.objects.select_related("usuario").order_by("-fecha")
    return render(request, "reportes/historial.html", {"registros": registros})


def reporte_autor_por_cedula(request):
    autor = None
    libros = []
    cedula = request.GET.get("cedula", "")

    if cedula:
        try:
            autor = Autor.objects.get(cedula=cedula)
            libros = autor.libros.all()
        except Autor.DoesNotExist:
            autor = None
            libros = []

    return render(
        request,
        "reportes/reporte_autor.html",
        {"autor": autor, "libros": libros, "cedula": cedula},
    )
