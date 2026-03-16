from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Perfil
from .forms import UsuarioForm
from reportes.views import registrar_actividad


def login_usuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect("inicio")
        else:
            return render(
                request,
                "usuarios/login.html",
                {"error": "Usuario o contraseña incorrectos"},
            )

    return render(request, "usuarios/login.html")


def logout_usuario(request):
    logout(request)
    return redirect("login")

    def es_admin(user):
        return hasattr(user, "perfil") and user.perfil.rol == "ADMIN"


def lista_usuarios(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    usuarios = User.objects.all().select_related("perfil")
    return render(request, "usuarios/lista.html", {"usuarios": usuarios})


def crear_usuario(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)

            password = form.cleaned_data["password"]
            if password:
                usuario.set_password(password)

            usuario.save()

            perfil, created = Perfil.objects.get_or_create(usuario=usuario)
            perfil.rol = form.cleaned_data["rol"]
            perfil.save()

            registrar_actividad(
                request.user,
                "CREAR",
                "Usuario",
                f"Se creó el usuario {usuario.username} con rol {perfil.get_rol_display()}",
            )

            return redirect("lista_usuarios")
    else:
        form = UsuarioForm()

    return render(
        request, "usuarios/form.html", {"form": form, "titulo": "Crear usuario"}
    )


def editar_usuario(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    usuario = get_object_or_404(User, id=id)
    perfil, created = Perfil.objects.get_or_create(usuario=usuario)

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)

            password = form.cleaned_data["password"]
            if password:
                usuario.set_password(password)

            usuario.save()

            perfil.rol = form.cleaned_data["rol"]
            perfil.save()

            registrar_actividad(
                request.user,
                "EDITAR",
                "Usuario",
                f"Se editó el usuario {usuario.username} y se asignó rol {perfil.get_rol_display()}",
            )

            return redirect("lista_usuarios")
    else:
        initial_data = {"rol": perfil.rol}
        form = UsuarioForm(instance=usuario, initial=initial_data)

    return render(
        request, "usuarios/form.html", {"form": form, "titulo": "Editar usuario"}
    )


def eliminar_usuario(request, id):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "ADMIN":
        return HttpResponseForbidden("No tienes permisos para esta acción")

    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        nombre_usuario = usuario.username
        registrar_actividad(
            request.user,
            "ELIMINAR",
            "Usuario",
            f"Se eliminó el usuario {nombre_usuario}",
        )
        usuario.delete()
        return redirect("lista_usuarios")

    return render(request, "usuarios/eliminar.html", {"usuario_obj": usuario})
