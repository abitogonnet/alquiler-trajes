from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Alquiler
from .forms import AlquilerCreateForm
from prendas.models import Prenda

def _set_prendas_estado(prendas, estado):
    for p in prendas:
        p.estado = estado
        p.save()

def _whatsapp_msg(alquiler: Alquiler) -> str:
    prendas = alquiler.prendas.all().order_by("tipo", "codigo")
    lines = []
    lines.append(f"ABITO - Confirmación de alquiler #{alquiler.id}")
    lines.append(f"Cliente: {alquiler.cliente_nombre}")
    lines.append(f"Tel: {alquiler.cliente_telefono}")
    lines.append("")
    lines.append("Prendas:")
    for p in prendas:
        lines.append(f"- {p.codigo}: {p.descripcion}")
    if alquiler.ruedo_saco:
        lines.append(f"Ruedo saco: {alquiler.ruedo_saco}")
    if alquiler.ruedo_pantalon:
        lines.append(f"Ruedo pantalón: {alquiler.ruedo_pantalon}")
    if alquiler.notas:
        lines.append(f"Notas: {alquiler.notas}")

    lines.append("")
    lines.append(f"Visita: {alquiler.fecha_visita.strftime('%d/%m/%Y')}")
    lines.append(f"Reserva: {alquiler.fecha_reserva.strftime('%d/%m/%Y')}")
    lines.append(f"Retiro (entrega): {alquiler.fecha_entrega.strftime('%d/%m/%Y')}")
    lines.append(f"Devolución: {alquiler.fecha_devolucion.strftime('%d/%m/%Y')}")
    lines.append("")
    lines.append(f"Seña: ${alquiler.senia_monto} ({alquiler.senia_metodo})")
    lines.append(f"Total: ${alquiler.total}")
    lines.append(f"Saldo al retirar: ${alquiler.saldo_restante} ({alquiler.saldo_metodo})")
    return "\n".join(lines)

def crear_alquiler(request):
    if request.method == "POST":
        form = AlquilerCreateForm(request.POST)
        if form.is_valid():
            prendas = form.cleaned_data["_prendas_objs"]
            fe = form.cleaned_data["fecha_entrega"]
            fd = form.cleaned_data["fecha_devolucion"]

            conflictos = (
                Alquiler.objects.filter(estado__in=["Reservado", "Entregado"])
                .filter(prendas__in=prendas)
                .filter(fecha_entrega__lte=fd, fecha_devolucion__gte=fe)
                .distinct()
            )
            if conflictos.exists():
                return render(request, "alquileres/crear.html", {
                    "form": form,
                    "conflictos": conflictos,
                })

            alquiler = form.save(commit=False)
            alquiler.estado = "Reservado"
            # si no cargan saldo, lo calculamos
            if alquiler.saldo_restante == 0 and alquiler.total and alquiler.senia_monto:
                alquiler.saldo_restante = max(alquiler.total - alquiler.senia_monto, 0)
            alquiler.save()
            alquiler.prendas.set(prendas)

            _set_prendas_estado(prendas, "Reservado")

            msg = _whatsapp_msg(alquiler)
            return render(request, "alquileres/creado.html", {"alquiler": alquiler, "wa_message": msg})
    else:
        form = AlquilerCreateForm(initial={"fecha_reserva": timezone.localdate()})

    return render(request, "alquileres/crear.html", {"form": form})

def listar_alquileres(request):
    alquileres = Alquiler.objects.all().order_by("fecha_entrega", "id")
    return render(request, "alquileres/listar.html", {"alquileres": alquileres})

def cambiar_estado(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    if request.method == "POST":
        nuevo = request.POST.get("estado")
        if nuevo in ["Reservado", "Entregado", "Disponible"]:
            alquiler.estado = nuevo
            alquiler.save()
            # sincronizamos prendas
            if nuevo == "Disponible":
                _set_prendas_estado(alquiler.prendas.all(), "Disponible")
            elif nuevo == "Entregado":
                _set_prendas_estado(alquiler.prendas.all(), "Entregado")
            else:
                _set_prendas_estado(alquiler.prendas.all(), "Reservado")
    return redirect("/alquileres/listar/")

def borrar_alquiler(request, alquiler_id):
    alquiler = get_object_or_404(Alquiler, id=alquiler_id)
    if request.method == "POST":
        # al borrar, liberamos prendas
        _set_prendas_estado(alquiler.prendas.all(), "Disponible")
        alquiler.delete()
        return redirect("/alquileres/listar/")
    return render(request, "alquileres/borrar.html", {"alquiler": alquiler})

def entregas(request):
    f1 = request.GET.get("desde")
    f2 = request.GET.get("hasta")
    qs = Alquiler.objects.none()
    if f1 and f2:
        qs = Alquiler.objects.filter(fecha_entrega__range=[f1, f2]).order_by("fecha_entrega")
    return render(request, "alquileres/entregas.html", {"alquileres": qs})

def devoluciones(request):
    f1 = request.GET.get("desde")
    f2 = request.GET.get("hasta")
    hoy = timezone.localdate()

    qs = Alquiler.objects.none()
    atrasados = Alquiler.objects.filter(estado__in=["Reservado", "Entregado"], fecha_devolucion__lt=hoy).order_by("fecha_devolucion")

    if f1 and f2:
        qs = Alquiler.objects.filter(fecha_devolucion__range=[f1, f2]).order_by("fecha_devolucion")

    return render(request, "alquileres/devoluciones.html", {"alquileres": qs, "atrasados": atrasados})
