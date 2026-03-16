from django.db import models
from django.contrib.auth.models import User


class RegistroActividad(models.Model):
    ACCIONES = [
        ("CREAR", "Crear"),
        ("EDITAR", "Editar"),
        ("ELIMINAR", "Eliminar"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    entidad = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.accion} - {self.entidad}"
