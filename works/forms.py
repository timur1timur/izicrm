from django import forms
from .models import Work


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['type_work', 'name', 'price']

        widgets = {
            "type_work": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите название работ"
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Стоимость работ"
                }
            )
        }