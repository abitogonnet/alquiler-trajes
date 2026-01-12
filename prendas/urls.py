from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_prenda, name="crear_prenda"),
    path("stock/", views.ver_stock, name="ver_stock"),
    path("disponibilidad/", views.ver_disponibilidad, name="ver_disponibilidad"),
]
