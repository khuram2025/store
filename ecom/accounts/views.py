from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, ResetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
import random
from .models import Account

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from .forms import LoginForm

from .models import UserProfile

def accounts(request):
    return render(request, 'pwa/accounts/account.html',)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Redirect to a 'login' page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


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

    return render(request, 'pwa/accounts/login.html', {'form': form})



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


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
from .forms import ResetPasswordForm
import random

def reset_password_request_view(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        user = Account.objects.filter(mobile_number=mobile_number).first()

        if user:
            otp = random.randint(100000, 999999)
            print(f"OTP for reset password: {otp}")  # Prints OTP on console
            request.session['reset_password_otp'] = str(otp)
            request.session['reset_password_user_id'] = user.id
            return redirect('accounts:verify_otp', user_id=user.id)
        else:
            # Handle case when user with entered mobile number does not exist
            return HttpResponse("No user with this mobile number.", status=404)

    return render(request, 'accounts/reset_password_request.html')


def verify_otp_view(request, user_id):
    stored_otp = request.session.get('reset_password_otp')

    if request.method == 'POST':
        otp = "".join(request.POST.getlist('otp'))  # concatenate all inputs

        if otp == stored_otp:
            return redirect('accounts:reset_password', user_id=user_id)
        else:
            return HttpResponse("Invalid OTP.", status=400)

    return render(request, 'accounts/verify_otp.html', {"user_id": user_id})


def reset_password_view(request, user_id):
    user = Account.objects.get(pk=user_id)
    if user is None:
        return HttpResponse("No user found for the provided id.", status=404)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirmation = form.cleaned_data.get('password_confirmation')
            if password and password == password_confirmation:
                user.set_password(password)
                user.save()
                return redirect('accounts:login')
            else:
                return HttpResponse("Passwords do not match.", status=400)
        else:
            # Handle form validation errors
            return HttpResponse(form.errors.as_json(), status=400)
    else:
        form = ResetPasswordForm()

    context = {"form": form, "user_id": user_id}
    return render(request, 'accounts/reset_password.html', context)
