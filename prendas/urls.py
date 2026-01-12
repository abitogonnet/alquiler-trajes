from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_prenda, name="crear_prenda"),
    path("listar/", views.listar_prendas, name="listar_prendas"),
    path("disponibilidad/", views.disponibilidad, name="disponibilidad"),
]
