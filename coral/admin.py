from django.contrib import admin

# Register your models here.
from coral.models import Coral, Photos


class coralAdmin(admin.ModelAdmin):
    model = Coral
    list_display = ['id','name', 'description', 'status', 'source','purchaseDate','purchaseCost','image','date_created','user']
    #list_display = [field.name for field in Coral._meta.get_fields()]
    list_filter = ['status', 'source', 'purchaseDate']
    list_editable = ['name', 'description', 'status', 'source']
class photoAdmin(admin.ModelAdmin):

    list_display = ('coral', 'image_date', 'images')

admin.site.register(Coral, coralAdmin)
admin.site.register(Photos, photoAdmin)






