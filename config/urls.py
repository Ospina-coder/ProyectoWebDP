from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from autores.models import Autor
from libros.models import Libro
from django.contrib.auth.models import User
from django.db.models import Count
from graphene_django.views import GraphQLView


@login_required
def inicio(request):

    total_autores = Autor.objects.count()
    total_libros = Libro.objects.count()
    total_usuarios = User.objects.count()

    autores_con_libros = Autor.objects.annotate(cantidad_libros=Count("libros"))

    nombres_autores = [autor.nombre for autor in autores_con_libros]
    cantidades_libros = [autor.cantidad_libros for autor in autores_con_libros]

    context = {
        "total_autores": total_autores,
        "total_libros": total_libros,
        "total_usuarios": total_usuarios,
        "nombres_autores": nombres_autores,
        "cantidades_libros": cantidades_libros,
    }

    return render(request, "inicio.html", context)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("usuarios/", include("usuarios.urls")),
    path("autores/", include("autores.urls")),
    path("libros/", include("libros.urls")),
    path("reportes/", include("reportes.urls")),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]
