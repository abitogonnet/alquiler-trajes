from django.db import models

class Gasto(models.Model):
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.fecha} - ${self.monto} - {self.descripcion}"
