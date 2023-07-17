from django.contrib import admin

# Register your models here.


from dashboard.models import apexMeasurments


class apexMeasurments_Admin(admin.ModelAdmin):
    list_display = [field.name for field in apexMeasurments._meta.get_fields()]

admin.site.register(apexMeasurments, apexMeasurments_Admin)