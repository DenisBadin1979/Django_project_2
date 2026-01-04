from django.contrib import admin

from .models import Payment, User

admin.site.register(User)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_method",
    )
    list_filter = (
        "user",
        "payment_method",
    )
    search_fields = ("user",)
