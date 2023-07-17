from django.urls import path
from coral import views

from .views import  CreateCoralView # new
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path("coral_list", views.index, name="index"),
    path("<int:pk>/", views.coral_detail, name="coral_detail"),
    path("newCoral/", CreateCoralView.as_view(), name="newCoral"),
    path("<int:pk>/photoUpdate", views.UpdatePhotoView.as_view(),name="photoUpdate"),
    path("<int:pk>/coralUpdate", views.UpdateCoralView.as_view(),name="coralUpdate"),
    path("<int:pk>/coralDelete",views.DeleteCoralView.as_view(),name="coralDelete"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)






