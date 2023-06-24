from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Redirect to a 'login' page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from .forms import LoginForm

from .models import UserProfile
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=mobile_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')  # Redirect to a 'home' page after successful login
            else:
                # return an 'invalid login' error message
                ...
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def profile_detail_view(request, pk):
    try:
        profile = UserProfile.objects.get(pk=pk)
        print("UserProfile object: ", profile)  # Debugging print statement
        print("Associated User object: ", profile.user)  # Debugging print statement
    except UserProfile.DoesNotExist:
        raise Http404("No UserProfile matches the given query.")
    return render(request, 'accounts/profile.html', {'profile': profile})


from django.views.generic import UpdateView
from .forms import UserProfileForm
from .models import UserProfile

def edit_profile(request, pk): 
    profile = UserProfile.objects.get(id=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile-detail', pk=profile.user.pk)

        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
    'form': form,
    'profile': profile  # Add this line
}
    return render(request, 'accounts/edit_profile.html', context)

