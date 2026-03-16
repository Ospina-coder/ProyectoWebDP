from django.urls import path
from . import views

urlpatterns = [
    path("autor/", views.reporte_autor_por_cedula, name="reporte_autor"),
    path("historial/", views.historial_actividad, name="historial_actividad"),
    path(
        "historial/eliminar/<int:id>/",
        views.eliminar_registro_actividad,
        name="eliminar_registro_actividad",
    ),
]
