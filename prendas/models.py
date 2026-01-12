from django.db import models

class Prenda(models.Model):
    TIPO_CHOICES = [
        ('Saco', 'Saco'),
        ('Pantalón', 'Pantalón'),
        ('Camisa', 'Camisa'),
        ('Chaleco', 'Chaleco'),
        ('Moño', 'Moño'),
        ('Corbata', 'Corbata'),
        ('Zapatos', 'Zapatos'),
    ]

    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Reservado', 'Reservado'),
        ('Entregado', 'Entregado'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    color = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    talle = models.CharField(max_length=10)
    codigo = models.CharField(max_length=10, unique=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Disponible')

    def save(self, *args, **kwargs):
        if not self.codigo:
            iniciales = (self.tipo[:2] if self.tipo else "XX").upper()

            # buscamos el último código bien formado para ese tipo
            ultimo = Prenda.objects.filter(tipo=self.tipo, codigo__regex=r"^[A-Z]{2}-\d{3}$").order_by("-codigo").first()

            numero = 1
            if ultimo and ultimo.codigo:
                try:
                    numero = int(ultimo.codigo.split("-")[1]) + 1
                except Exception:
                    numero = 1

            self.codigo = f"{iniciales}-{numero:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} {self.color} {self.marca} talle {self.talle} - {self.codigo}"
