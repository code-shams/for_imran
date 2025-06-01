from django import forms
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Car
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Car, Comment
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Purchase
from .forms import PurchaseForm



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


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    comments = car.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            if request.user.is_authenticated:
                comment.user = request.user
                comment.guest_name = None
            else:
                comment.user = None
            comment.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CommentForm()

    if request.user.is_authenticated:
        form.fields['guest_name'].widget = forms.HiddenInput()

    return render(request, 'view_page.html', {
        'car': car,
        'comments': comments,
        'form': form
    })




@login_required
def buy_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity > car.quantity:
                messages.error(request, "Not enough stock available")
                return redirect('car_detail', pk=car.pk)
            
            # Create purchase
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.car = car
            purchase.quantity = quantity
            purchase.total_price = car.price * quantity
            purchase.save()
            
            # Update car quantity
            car.quantity -= quantity
            car.save()
            
            messages.success(request, "Purchase completed successfully!")
            return redirect('homepage')
    else:
        quantity = int(request.GET.get('quantity', 1))
        form = PurchaseForm(initial={
            'payment_method': 'credit_card'
        })
    
    return render(request, 'buy_page.html', {
        'car': car,
        'form': form,
        'quantity': quantity,
        'total_price': car.price * quantity,
        'user': request.user
    })