from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    path("prendas/", include("prendas.urls")),
    path("alquileres/", include("alquileres.urls")),
    path("gastos/", include("gastos.urls")),
    path("reportes/", include("reportes.urls")),
]
