from django import forms
from .models import StorageItemTextile


class StorageTextileForm(forms.ModelForm):
    class Meta:
        model = StorageItemTextile
        fields = ['item', 'quantity', 'price', 'price_f']
        widgets = {
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "price_f": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            )
        }