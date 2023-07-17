from django.contrib import admin

# Register your models here.
from sales.models import coral_sale


class coral_sale_Admin(admin.ModelAdmin):
    list_display = [field.name for field in coral_sale._meta.get_fields()]
    list_filter = ['species', 'sale_date']
    list_editable = ['coral_name', 'user', 'sale_price', 'sale_date']
admin.site.register(coral_sale, coral_sale_Admin)
