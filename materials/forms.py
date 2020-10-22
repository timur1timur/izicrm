from django import forms
from .models import TextileManufact, CorniceManufact, Textile, Cornice, TextileCollection, CorniceCollection


class TextileManufactForm(forms.ModelForm):
    class Meta:
        model = TextileManufact
        fields = ['name', 'email']

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите название компании"
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "email компании"
                }
            )
        }

class TextileCollectionForm(forms.ModelForm):
    class Meta:
        model = TextileCollection
        fields = ['name', 'manufacturer']

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите название коллекции"
                }
            ),
            "manufacturer": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }

class CorniceManufactForm(forms.ModelForm):
    class Meta:
        model = CorniceManufact
        fields = ['name', 'email']

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите название компании"
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "email компании"
                }
            )
        }

class CorniceCollectionForm(forms.ModelForm):
    class Meta:
        model = CorniceCollection
        fields = ['name', 'manufacturer']

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите название коллекции"
                }
            ),
            "manufacturer": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }

class TextileForm(forms.ModelForm):
    class Meta:
        model = Textile
        fields = ['manufacturer', 'collection', 'model', 'color', 'height', 'price_opt', 'price_pog', 'price_rul']

        widgets = {
            "manufacturer": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",

                }
            ),
            "collection": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",

                }
            ),
            "model": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Название ткани"
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цвет ткани"
                }
            ),
            "height": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Высота ткани"
                }
            ),
            "price_opt": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цена оптовая"
                }
            ),
            "price_pog": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цена пог.метра"
                }
            ),
            "price_rul": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цена рулона"
                }
            ),
        }

class CorniceForm(forms.ModelForm):
    class Meta:
        model = Cornice
        fields = ['manufacturer', 'collection', 'model', 'long', 'price_opt', 'price_pog']

        widgets = {
            "manufacturer": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",

                }
            ),
            "collection": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",

                }
            ),
            "model": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Название карниза"
                }
            ),
            "long": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Длина карниза"
                }
            ),
            "price_opt": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цена оптовая"
                }
            ),
            "price_pog": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цена пог.метра"
                }
            )

        }