from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    """Создание заказов"""

    post_code = USZipCodeField()

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "post_code", "city"]
