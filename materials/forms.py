from django import forms
from .models import TextileManufact, CorniceManufact, Textile, Cornice, TextileCollection, CorniceCollection, \
    CorniceAdditional, CorniceCollectionColor, CorniceAdditionalOptions


class TextileManufactForm(forms.ModelForm):
    class Meta:
        model = TextileManufact
        fields = ['name', 'email', 'phone', 'manager', 'type_p']

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
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "телефон компании"
                }
            ),
            "manager": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "менеджер"
                }
            ),
            "type_p": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "менеджер"
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
        fields = ['name', 'email', 'phone', 'manager', 'type_p']

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
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "телефон компании"
                }
            ),
            "manager": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "менеджер"
                }
            ),
            "type_p": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "менеджер"
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
        fields = ['manufacturer', 'collection', 'model', 'color', 'height', 'price_opt', 'article']

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
            "article": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Артикул"
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
        fields = ['manufacturer', 'collection', 'model', 'long', 'price_opt']

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


class CorniceAdditionalForm(forms.ModelForm):
    class Meta:
        model = CorniceAdditional
        fields = ['collection', 'category', 'name']

        widgets = {
            "collection": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",

                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Категория"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Наименование"
                }
            )
        }

class CorniceCollectionColorForm(forms.ModelForm):
    class Meta:
        model = CorniceCollectionColor
        fields = ['color']

        widgets = {
            "color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Цвет"
                }
            )
        }


class CorniceAdditionalOptionsForm(forms.ModelForm):
    class Meta:
        model = CorniceAdditionalOptions
        fields = ['type_p', 'price']

        widgets = {
            "type_p": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Тип"
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Стоимость"
                }
            )
        }