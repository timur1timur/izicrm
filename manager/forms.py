from django import forms
from .models import SupplierOrderedTextile, SupplierOrderedCornice
from orders.models import Payment

class SupplierOrderedTextileForm(forms.ModelForm):

    class Meta:
        model = SupplierOrderedTextile
        fields = ['order', 'item', 'price', 'receipt', 'status', 'date_shipped']
        widgets = {
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите стоимость материала из счета"
                }
            ),
            "receipt": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите номер счета"
                }
            ),
            "date_shipped": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите номер счета"
                }
            )
        }


class SupplierOrderedCorniceForm(forms.ModelForm):

    class Meta:
        model = SupplierOrderedCornice
        fields = ['order', 'item', 'additional', 'price', 'receipt', 'status', 'date_shipped']
        widgets = {
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "additional": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите стоимость материала из счета"
                }
            ),
            "receipt": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите номер счета"
                }
            ),
            "date_shipped": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите дату отгрузки"
                }
            )
        }


class PaymentFormManager(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['order', 'customer', 'category', 'type_money', 'price', 'receipt']
        widgets = {
            "category": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select custom-select-sm",
                }
            ),
            "type_money": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select custom-select-sm",

                }
            ),
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите сумму платежа"
                }
            ),
            "receipt": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите номер чека"
                }
            )
        }

class SupplierForm(forms.Form):
    email = forms.CharField(max_length=2000)
    subject = forms.CharField(max_length=2000)
    text = forms.CharField(max_length=2000)

    class Meta:
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "type": "email",
                    "class": "form-control form-control-sm",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control form-control-sm",

                }
            ),
            "text": forms.Textarea(
                attrs={
                    "rows": 10,
                    "class": "form-control",
                    "placeholder": "Введите текст заказа"
                }
            )
        }