
from django.contrib import admin
from django.urls import path
from lendsqr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.users,)
]
