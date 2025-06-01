from django.urls import path
from . import views

urlpatterns = [
    path('homepage/',views.home, name='homepage'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/<int:pk>/buy/', views.buy_car, name='buy_car'),
]
