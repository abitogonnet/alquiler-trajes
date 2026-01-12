from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_gasto, name="crear_gasto"),
    path("listar/", views.listar_gastos, name="listar_gastos"),
]
