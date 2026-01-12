from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Prenda

# Para disponibilidad (si ya tenés alquileres)
try:
    from alquileres.models import Alquiler
except Exception:
    Alquiler = None


def crear_prenda(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        color = request.POST.get("color")
        marca = request.POST.get("marca")
        talle = request.POST.get("talle")

        if not (tipo and color and marca and talle):
            messages.error(request, "Faltan datos obligatorios.")
            return redirect("crear_prenda")

        p = Prenda(tipo=tipo, color=color, marca=marca, talle=talle, estado="Disponible")
        p.save()
        messages.success(request, f"Prenda creada: {p.codigo}")
        return redirect("crear_prenda")

    return render(request, "prendas/crear_prenda.html")


def ver_stock(request):
    # Filtros
    tipo = (request.GET.get("tipo") or "").strip()
    estado = (request.GET.get("estado") or "").strip()
    q = (request.GET.get("q") or "").strip()

    prendas = Prenda.objects.all()

    if tipo:
        prendas = prendas.filter(tipo=tipo)

    if estado:
        prendas = prendas.filter(estado=estado)

    if q:
        prendas = prendas.filter(
            Q(codigo__icontains=q)
            | Q(color__icontains=q)
            | Q(marca__icontains=q)
            | Q(talle__icontains=q)
        )

    prendas = prendas.order_by("tipo", "codigo")

    ctx = {
        "prendas": prendas,
        "tipos": [x[0] for x in Prenda.TIPO_CHOICES],
        "estados": [x[0] for x in Prenda.ESTADO_CHOICES],
        "tipo_sel": tipo,
        "estado_sel": estado,
        "q": q,
        "total": prendas.count(),
    }
    return render(request, "prendas/stock.html", ctx)


def ver_disponibilidad(request):
    """
    Pantalla: eliges fecha_inicio y fecha_fin y muestra prendas NO disponibles en ese rango.
    Requiere que exista el modelo Alquiler con M2M 'prendas' y campos fecha_entrega/fecha_devolucion/estado.
    """
    prendas_no_disp = []
    fecha_inicio = (request.GET.get("fecha_inicio") or "").strip()
    fecha_fin = (request.GET.get("fecha_fin") or "").strip()

    if Alquiler is None:
        messages.error(request, "No se encontró el módulo alquileres.models (ver disponibilidad no está listo).")
        return render(request, "prendas/disponibilidad.html", {"prendas_no_disp": [], "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})

    if fecha_inicio and fecha_fin:
        # Alquileres que se pisan con el rango y siguen activos
        alquileres = Alquiler.objects.filter(
            estado__in=["Reservado", "Entregado"]
        ).filter(
            Q(fecha_entrega__lte=fecha_fin) & Q(fecha_devolucion__gte=fecha_inicio)
        ).distinct()

        # Prendas ocupadas por esos alquileres
        prendas_no_disp = Prenda.objects.filter(alquiler__in=alquileres).distinct().order_by("tipo", "codigo")

    ctx = {
        "prendas_no_disp": prendas_no_disp,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    }
    return render(request, "prendas/disponibilidad.html", ctx)
