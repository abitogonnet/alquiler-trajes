import json

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek
from django.shortcuts import render

from alquileres.models import Alquiler


def dashboard(request):
    through = Alquiler.prendas.through  # tabla intermedia M2M (alquiler-prenda)

    # 1) Cantidad de prendas alquiladas por color / talle (ocurrencias en alquileres)
    por_color = list(
        through.objects.values("prenda__color")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    por_talle = list(
        through.objects.values("prenda__talle")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # 2) Montos por método de pago
    senias_por_metodo = list(
        Alquiler.objects.values("senia_metodo")
        .annotate(monto=Sum("senia_monto"))
        .order_by("-monto")
    )
    saldo_cobrado_por_metodo = list(
        Alquiler.objects.filter(estado__in=["Entregado", "Disponible"])
        .values("saldo_metodo")
        .annotate(monto=Sum("saldo_restante"))
        .order_by("-monto")
    )

    # 3) Cantidad de alquileres por mes / semana (según fecha_entrega)
    cant_por_mes = list(
        Alquiler.objects.annotate(m=TruncMonth("fecha_entrega"))
        .values("m")
        .annotate(total=Count("id"))
        .order_by("m")
    )
    cant_por_semana = list(
        Alquiler.objects.annotate(w=TruncWeek("fecha_entrega"))
        .values("w")
        .annotate(total=Count("id"))
        .order_by("w")
    )

    # 4) Monto total por mes / semana (según fecha_entrega)
    monto_por_mes = list(
        Alquiler.objects.annotate(m=TruncMonth("fecha_entrega"))
        .values("m")
        .annotate(monto=Sum("total"))
        .order_by("m")
    )
    monto_por_semana = list(
        Alquiler.objects.annotate(w=TruncWeek("fecha_entrega"))
        .values("w")
        .annotate(monto=Sum("total"))
        .order_by("w")
    )

    ctx = {
        "por_color": json.dumps({
            "labels": [x["prenda__color"] or "Sin color" for x in por_color],
            "data": [x["total"] for x in por_color],
        }),
        "por_talle": json.dumps({
            "labels": [x["prenda__talle"] or "Sin talle" for x in por_talle],
            "data": [x["total"] for x in por_talle],
        }),
        "senias_por_metodo": json.dumps({
            "labels": [x["senia_metodo"] or "Sin método" for x in senias_por_metodo],
            "data": [float(x["monto"] or 0) for x in senias_por_metodo],
        }),
        "saldo_por_metodo": json.dumps({
            "labels": [x["saldo_metodo"] or "Sin método" for x in saldo_cobrado_por_metodo],
            "data": [float(x["monto"] or 0) for x in saldo_cobrado_por_metodo],
        }),
        "cant_por_mes": json.dumps({
            "labels": [x["m"].strftime("%Y-%m") for x in cant_por_mes if x["m"]],
            "data": [x["total"] for x in cant_por_mes if x["m"]],
        }),
        "cant_por_semana": json.dumps({
            "labels": [x["w"].strftime("%Y-%m-%d") for x in cant_por_semana if x["w"]],
            "data": [x["total"] for x in cant_por_semana if x["w"]],
        }),
        "monto_por_mes": json.dumps({
            "labels": [x["m"].strftime("%Y-%m") for x in monto_por_mes if x["m"]],
            "data": [float(x["monto"] or 0) for x in monto_por_mes if x["m"]],
        }),
        "monto_por_semana": json.dumps({
            "labels": [x["w"].strftime("%Y-%m-%d") for x in monto_por_semana if x["w"]],
            "data": [float(x["monto"] or 0) for x in monto_por_semana if x["w"]],
        }),
    }
    return render(request, "reportes/dashboard.html", ctx)
