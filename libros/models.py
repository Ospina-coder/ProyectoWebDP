from django.db import models
from autores.models import Autor


class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    editorial = models.CharField(max_length=100)
    anio_publicacion = models.PositiveIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")
    portada_url = models.URLField(blank=True, null=True)
    titulo_api = models.CharField(max_length=200, blank=True, null=True)
    editorial_api = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.titulo
