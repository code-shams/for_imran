from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Car
from django.shortcuts import render

class CarCreateView(UserPassesTestMixin, CreateView):
    model = Car
    fields = '__all__'
    template_name = 'cars/add_car.html'
    success_url = reverse_lazy('car_list')  # change to your success url

    def test_func(self):
        return self.request.user.is_staff  # only staff/admin can access

def home(request):
    cars = Car.objects.all()
    return render(request,'homepage.html', {'cars': cars})