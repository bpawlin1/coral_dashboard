from django.urls import path
from sales import views
from django.conf import settings
from django.conf.urls.static import static
from .views import  CreateCoralSale # new

urlpatterns = [
 
    path("", views.sales, name="sales"),
    path("newSale/", CreateCoralSale.as_view(), name="newSale"),
    path("tables/", views.sale_tables, name="tables"),

] 

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)






