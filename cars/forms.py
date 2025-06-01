from django import forms
from .models import Car
from .models import Comment
from .models import Purchase

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['guest_name', 'text']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border-2 border-[#ffcbde] rounded-lg mb-2',
                'placeholder': 'Your name'
            }),
            'text': forms.Textarea(attrs={
                'class': 'w-full p-4 border-2 border-[#ffcbde] rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }



class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['shipping_address', 'payment_method']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full p-2 border-2 border-[#ffcbde] rounded-lg mb-4',
                'placeholder': 'Enter your shipping address.'
            }),
        }