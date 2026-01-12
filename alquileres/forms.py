from django import forms
from django.utils import timezone

from .models import Alquiler
from prendas.models import Prenda

class AlquilerCreateForm(forms.ModelForm):
    prendas_codigos = forms.CharField(
        label="Prendas (códigos separados por coma)",
        help_text="Ej: SA-000, PA-012, CA-003",
    )

    class Meta:
        model = Alquiler
        fields = [
            "cliente_nombre", "cliente_telefono",
            "fecha_visita", "fecha_reserva", "fecha_entrega", "fecha_devolucion",
            "prendas_codigos",
            "ruedo_saco", "ruedo_pantalon", "notas",
            "senia_monto", "senia_metodo",
            "total",
            "saldo_restante", "saldo_metodo",
        ]
        widgets = {
            "fecha_visita": forms.DateInput(attrs={"type": "date"}),
            "fecha_reserva": forms.DateInput(attrs={"type": "date"}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}),
            "fecha_devolucion": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get("fecha_reserva"):
            self.initial["fecha_reserva"] = timezone.localdate()

    def clean_prendas_codigos(self):
        raw = self.cleaned_data["prendas_codigos"]
        codigos = [x.strip().upper() for x in raw.split(",") if x.strip()]
        if not codigos:
            raise forms.ValidationError("Tenés que ingresar al menos 1 código de prenda.")

        prendas = list(Prenda.objects.filter(codigo__in=codigos))
        encontrados = {p.codigo for p in prendas}
        faltan = [c for c in codigos if c not in encontrados]
        if faltan:
            raise forms.ValidationError(f"Estos códigos no existen: {', '.join(faltan)}")

        self.cleaned_data["_prendas_objs"] = prendas
        return raw

    def clean(self):
        cleaned = super().clean()
        fe = cleaned.get("fecha_entrega")
        fd = cleaned.get("fecha_devolucion")
        if fe and fd and fd < fe:
            self.add_error("fecha_devolucion", "La devolución no puede ser antes de la entrega.")
        return cleaned
