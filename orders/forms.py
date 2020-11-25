from django import forms
from .models import Specification, OrderItemTextile1, OrderItemCornice, OrderItemWorkSewing, OrderItemWorkAssembly, \
    Room, Customer, Contract, Payment, SupplierOrder, Order, OrderItemWorkHanging, OrderItemWorkDelivery, \
    PaymentCategory, OrderItemCorniceAdditional
from works.models import Work

SOURCE_T = (
    (0, 'От Партнеров'),
    (1, 'Социальные сети'),
    (2, 'Маркетплейс'),
    (3, 'Телефон'),
    (4, 'Салон'),
)

class CustomerStartForm(forms.ModelForm):
    source = forms.ChoiceField(widget=forms.RadioSelect, choices=SOURCE_T)

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        widgets = {
            "source": forms.RadioSelect(
                attrs={
                    "type": "Radio",
                    "class": "custom-control-input",

                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите ФИО заказчика"
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите телефон"
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите email"
                }
            )
        }


class SupplierOrderForm(forms.ModelForm):
    class Meta:
        model = SupplierOrder
        fields = '__all__'

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['order', 'customer', 'category', 'type_money', 'price', 'receipt', 'user']
        widgets = {
            "category": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
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

class PaymentFormDirector(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentFormDirector, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = PaymentCategory.objects.filter(type_p=1)

    class Meta:
        model = Payment
        fields = ['order', 'customer', 'category', 'type_money', 'price', 'receipt']
        widgets = {
            "category": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
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

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['order', 'customer', 'price', 'garant', 'prepay', 'prepay_duration', 'work_start', 'work_duration',
                  'date_acceptance', 'date_finish']
        widgets = {
            "price": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите номер чека"
                }
            ),
            "garant": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите гарантийный срок"
                }
            ),
            "prepay": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите размер предоплаты"
                }
            ),
            "prepay_duration": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Предоплата в течении ... дней"
                }
            ),
            "work_start": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Начать работу через ... дней"
                }
            ),
            "work_duration": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите количество дней"
                }
            ),
            "date_acceptance": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите дату"
                }
            ),
            "date_finish": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите дату"
                }
            ),

        }

class CustomerForm(forms.ModelForm):
    source = forms.ChoiceField(widget=forms.RadioSelect, choices=SOURCE_T)
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите ФИО"
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите телефон"
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите email"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите адрес заказчика"
                }
            ),
            "pass_series": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Серия"
                }
            ),
            "pass_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Номер"
                }
            ),
            "pass_date": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Дата выдачи"
                }
            ),
            "pass_issued": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Кем выдан"
                }
            ),
            "source": forms.RadioSelect(
                attrs={
                    "type": "Radio",
                    "class": "custom-control-input",

                }
            ),
            "source_t": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )

        }


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите ФИО"
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите телефон"
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите email"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Введите адрес заказчика"
                }
            ),
            "pass_series": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Серия"
                }
            ),
            "pass_number": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Номер"
                }
            ),
            "pass_date": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Дата выдачи"
                }
            ),
            "pass_issued": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Кем выдан"
                }
            ),

            "source_t": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select custom-select-sm",
                }
            )

        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'order']

        widgets = {
            "order": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Помещение"
                }
            )
        }


SP_V = (
    ('Econom', 'Econom'),
    ('Standart', 'Standart'),
    ('Premium', 'Premium')
)

class SpecificationForm(forms.ModelForm):
    source = forms.ChoiceField(widget=forms.RadioSelect, choices=SP_V)
    class Meta:
        model = Specification
        fields = ['version', 'order', 'room']
        widgets = {
            "source": forms.RadioSelect(
                attrs={
                    "type": "Radio",
                    "class": "custom-control-input",
                }
            )
        }


class OrderTextileForm(forms.ModelForm):
    class Meta:
        model = OrderItemTextile1
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
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

class OrderCorniceForm(forms.ModelForm):
    class Meta:
        model = OrderItemCornice
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
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

class OrderCorniceAdditionalForm(forms.ModelForm):
    class Meta:
        model = OrderItemCorniceAdditional
        fields = ['specification', 'order', 'item', 'quantity', 'color', 'markup']
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            )
        }

class OrderWorkSewingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderWorkSewingForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Work.objects.filter(type_work__name='Пошив')

    class Meta:
        model = OrderItemWorkSewing
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }


class OrderWorkAssemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderWorkAssemblyForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Work.objects.filter(type_work__name='Монтаж')

    class Meta:
        model = OrderItemWorkAssembly
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }

class OrderWorkHangingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderWorkHangingForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Work.objects.filter(type_work__name='Развеска штор')

    class Meta:
        model = OrderItemWorkHanging
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }


class OrderWorkDeliveryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderWorkDeliveryForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Work.objects.filter(type_work__name='Доставка')

    class Meta:
        model = OrderItemWorkDelivery
        fields = ['specification', 'order', 'item', 'quantity', 'markup']
        widgets = {
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "item": forms.Select(
                attrs={
                    "type": "Select",
                    "class": "custom-select",
                }
            )
        }