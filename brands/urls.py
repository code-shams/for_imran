from django.urls import path
from . import views

urlpatterns = [
    path('brands/',views.add_brand, name='brands'),
]
