from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
    ]

    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default='EMPLEADO')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"