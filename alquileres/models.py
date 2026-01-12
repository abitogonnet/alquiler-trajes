from django.db import models
from prendas.models import Prenda

class Alquiler(models.Model):
    ESTADOS = [
        ("Reservado", "Reservado"),
        ("Entregado", "Entregado"),
        ("Disponible", "Disponible"),
    ]

    METODOS = [
        ("Efectivo", "Efectivo"),
        ("Transferencia", "Transferencia"),
        ("MercadoPago", "MercadoPago"),
        ("Tarjeta", "Tarjeta"),
    ]

    cliente_nombre = models.CharField(max_length=80)
    cliente_telefono = models.CharField(max_length=40)

    fecha_visita = models.DateField()
    fecha_reserva = models.DateField()
    fecha_entrega = models.DateField()
    fecha_devolucion = models.DateField()

    prendas = models.ManyToManyField(Prenda, related_name="alquileres")

    ruedo_saco = models.CharField(max_length=40, blank=True, default="")
    ruedo_pantalon = models.CharField(max_length=40, blank=True, default="")
    notas = models.TextField(blank=True, default="")

    senia_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    senia_metodo = models.CharField(max_length=20, choices=METODOS, default="Efectivo")

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    saldo_restante = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_metodo = models.CharField(max_length=20, choices=METODOS, default="Efectivo")

    estado = models.CharField(max_length=12, choices=ESTADOS, default="Reservado")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alquiler #{self.id} - {self.cliente_nombre} ({self.estado})"
