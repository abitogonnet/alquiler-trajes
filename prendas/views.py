from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import PrendaForm
from .models import Prenda
from alquileres.models import Alquiler  # para disponibilidad

def crear_prenda(request):
    if request.method == "POST":
        form = PrendaForm(request.POST)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.estado = "Disponible"
            prenda.save()
            return render(request, "prendas/creada.html", {"prenda": prenda})
    else:
        form = PrendaForm()
    return render(request, "prendas/crear.html", {"form": form})

def listar_prendas(request):
    prendas = Prenda.objects.order_by("tipo", "codigo")
    return render(request, "prendas/listar.html", {"prendas": prendas})

def disponibilidad(request):
    no_disponibles = []
    f1 = request.GET.get("desde")
    f2 = request.GET.get("hasta")

    if f1 and f2:
        activos = Alquiler.objects.filter(estado__in=["Reservado", "Entregado"]).filter(
            fecha_entrega__lte=f2,
            fecha_devolucion__gte=f1,
        )
        no_disponibles = Prenda.objects.filter(alquileres__in=activos).distinct().order_by("tipo", "codigo")

    return render(request, "prendas/disponibilidad.html", {"no_disponibles": no_disponibles})
