from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile
from cars.models import Purchase



def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)  # Form with submitted data
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Account created successfully :)')
            return redirect('profile')
        # If invalid, render the same form with errors
    else:
        register_form = forms.RegistrationForm()  # Empty form for GET requests
    
    return render(request, 'register.html', {'form': register_form, 'type': 'register'})



class UserLoginView(LoginView):
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'logged in incorrect')
        return super().form_invalid(form)        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'login'
        return context
    


def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Correct usage
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'pass_change.html', {'form': form})


def user_logout(request):
   logout(request)
   messages.success(request, 'You have been successfully logged out.')
   return redirect('user_login')


@login_required
def profile(request):
    # Get the user's purchases, ordered by most recent first
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchase_date')
    
    # Your existing form logic
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'purchases': purchases,  # Add purchases to the context
    }
    return render(request, 'profile.html', context)



@login_required
def edit_profile(request):
    user = request.user

    # Ensure profile exists
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    return render(request, 'edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

@login_required
def upload_profile_photo(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Profile photo updated!')
        else:
            messages.error(request, 'Failed to update profile photo.')
    return redirect('profile')
