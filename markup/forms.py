from django import forms
from .models import *


class MarkupCustomerCategoryForm(forms.ModelForm):

    class Meta:
        model = MarkupCustomerCategory
        fields = ['markup', 'source_t']
        widgets = {
            "source_t": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "markup": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите стоимость материала из счета"
                }
            )
        }

class MarkupMaterialCategoryForm(forms.ModelForm):

    class Meta:
        model = MarkupMaterialCategory
        fields = ['markup', 'source_t']
        widgets = {
            "source_t": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "markup": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите стоимость материала из счета"
                }
            )
        }

class MarkupWorkCategoryForm(forms.ModelForm):

    class Meta:
        model = MarkupWorkCategory
        fields = ['markup', 'source_t']
        widgets = {
            "source_t": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "markup": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите стоимость материала из счета"
                }
            )
        }