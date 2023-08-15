from django.urls import path
from django.conf.urls import url
from django.contrib.auth import login
from . import views
from django.urls import path, include
 



urlpatterns = [
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register), 
    path("explore", views.homepage, name = 'explore'), 
    path("profile", views.user_profile), 
    path("profile/<int:pk>", views.view_profile, name='profile'), 
    path("profile/update", views.update_profile, name='update_profile'), 
]