from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.aboutme),
    path('', views.landing),
]