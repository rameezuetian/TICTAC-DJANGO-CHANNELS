from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/<str:room_code>/', views.play, name='play'),
]
