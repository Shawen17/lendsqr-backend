
from django.contrib import admin
from django.urls import path
from lendsqr import views
from django.conf.urls.static import static 
from  django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',views.users,),
    path('api/filter-users/',views.filter_users),
]

urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)