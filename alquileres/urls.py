from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_alquiler, name="crear_alquiler"),
    path("listar/", views.listar_alquileres, name="listar_alquileres"),
    path("<int:alquiler_id>/estado/", views.cambiar_estado, name="cambiar_estado"),
    path("<int:alquiler_id>/borrar/", views.borrar_alquiler, name="borrar_alquiler"),
    path("entregas/", views.entregas, name="entregas"),
    path("devoluciones/", views.devoluciones, name="devoluciones"),
]
