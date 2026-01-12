from django.db import models

class Prenda(models.Model):
    TIPOS = [
        ("Saco", "Saco"),
        ("Pantalón", "Pantalón"),
        ("Camisa", "Camisa"),
        ("Chaleco", "Chaleco"),
        ("Moño", "Moño"),
        ("Corbata", "Corbata"),
        ("Zapatos", "Zapatos"),
    ]

    ESTADOS = [
        ("Disponible", "Disponible"),
        ("Reservado", "Reservado"),
        ("Entregado", "Entregado"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    color = models.CharField(max_length=40)
    marca = models.CharField(max_length=40, blank=True, default="")
    talle = models.CharField(max_length=20)

    codigo = models.CharField(max_length=10, unique=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="Disponible")

    created_at = models.DateTimeField(auto_now_add=True)

    def _prefix(self):
        return {
            "Saco": "SA",
            "Pantalón": "PA",
            "Camisa": "CA",
            "Chaleco": "CH",
            "Moño": "MO",
            "Corbata": "CO",
            "Zapatos": "ZA",
        }[self.tipo]

    def save(self, *args, **kwargs):
        if not self.codigo:
            prefix = self._prefix()
            last = Prenda.objects.filter(codigo__startswith=f"{prefix}-").order_by("-codigo").first()
            if last and "-" in last.codigo:
                n = int(last.codigo.split("-")[1]) + 1
            else:
                n = 0
            self.codigo = f"{prefix}-{n:03d}".upper()
        super().save(*args, **kwargs)

    @property
    def descripcion(self):
        marca_txt = f" {self.marca}" if self.marca else ""
        return f"{self.tipo} {self.color}{marca_txt} talle {self.talle}".strip()

    def __str__(self):
        return f"{self.codigo} - {self.descripcion} ({self.estado})"
