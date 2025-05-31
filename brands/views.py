from django.shortcuts import render, redirect
from . import forms

# Create your views here.

def add_brand(request):
    if request.method == 'POST':
        brand_form = forms.BrandForm(request.POST)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('add_brand')
    else:
        brand_form = forms.Brand()
    
    return render('request', 'add_brand.html', {'brand': brand_form})
            