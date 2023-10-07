from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    """Форма для ввода пользователем купона"""

    code = forms.CharField(label=_("Coupon"))
