import csv
import datetime
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    """Отображение заказов"""

    model = OrderItem
    raw_id_fields = ["product"]


def order_payment(obj):
    """Статус оплаты в страйп"""
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ""


order_payment.short_description = "Stripe payment"


def export_to_csv(modeladmin, request, queryset):
    """Скачивание спика заказов в формате csv"""
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"


def order_detail(obj):
    url = reverse("orders:admin_order_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse("orders:admin_order_pdf", args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = "Invoice"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Регистрация модели заказов в админ панеле"""

    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "post_code",
        order_payment,
        "city",
        "created",
        "updated",
        "paid",
        order_detail,
        order_pdf,
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
