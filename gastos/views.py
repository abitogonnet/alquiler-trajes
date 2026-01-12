from django.shortcuts import render, redirect
from .forms import GastoForm
from .models import Gasto

def crear_gasto(request):
    if request.method == "POST":
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/gastos/listar/")
    else:
        form = GastoForm()
    return render(request, "gastos/crear.html", {"form": form})

def listar_gastos(request):
    gastos = Gasto.objects.order_by("-fecha", "-id")
    return render(request, "gastos/listar.html", {"gastos": gastos})
