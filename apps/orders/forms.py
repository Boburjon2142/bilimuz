from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "extra_phone", "address", "note", "payment_type"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "F.I.Sh"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 90 123 45 67"}),
            "extra_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Qo‘shimcha raqam (ixtiyoriy)"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Manzil"}),
            "note": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "Izoh"}),
            "payment_type": forms.Select(attrs={"class": "form-select"}),
        }
