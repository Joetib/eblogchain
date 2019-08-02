from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pledge
from .forms import (
    ProfileForm,
    UserCreateForm,
    LoginForm,
    ContactForm,
    ProfileEditForm,
    PledgeForm,
    MomoRefNumberForm,
    )

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('app:welcome')
    return render(request, "index.html", {})


def signup(request):
    if request.user.is_authenticated:
        return redirect('app:welcome')
    if request.method=="POST":

        user_form = UserCreateForm(request.POST)

        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid and profile_form.is_valid:
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.momo_number = user.username
            profile.save()
            login(request, user)
            messages.success(request, message="Login Successful")
            return redirect('app:welcome')

        else:
            messages.error(request, message="Form is invalid")

    user_form = UserCreateForm()
    profile_form = ProfileForm()
    return render(request, "signup.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })

def loginview(request):
    if request.user.is_authenticated:
        return redirect('app:welcome')
    if request.method=="POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request=request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user=user)
                
                messages.success(request, message="Login Successful")
                return redirect('app:welcome')
            else:
                messages.error(request, "Log In failed")
        else:
            messages.error(request, message="Form is invalid")
    login_form = LoginForm()
    return render(request, "login.html", {'login_form': login_form,})

@login_required
def logout_view(request):
    logout(request)


@login_required
def welcome(request):
    
    return render(request, "welcome.html", {})


@login_required
def profile(request):
    if request.method=="POST":
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
    profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def history(request):
    next_payment_list = Pledge.objects.filter(
        paid=False,
        profile=request.user.profile
    )
    if request.method == "POST":
        if len(next_payment_list) >= 0:
            messages.error(request, "You already have a pending pledge")
        else:
            pledge_form = PledgeForm(request.POST)
            if pledge_form.is_valid():
                pledge_form.save()
                messages.success(request, "Pledge Successful. Please, enter momo Reference number for payment Confirmation")
                return redirect('app:momo_ref_confirm')

    pledge_form = PledgeForm()
    if len(next_payment_list) == 1:
        next_payment = next_payment_list[0]
    else:
        next_payment = None

    return render(request, 'history.html', {'pledge_form': pledge_form, 'next_payment': next_payment,})

@login_required
def momo_ref_confirm(request):
    next_payment_list = Pledge.objects.filter(
        paid=False,
        confirm_received=False,
        profile=request.user.profile
    )
    if len(next_payment_list) == 1:
        pledge = next_payment_list[0]
        if request.method=="POST":
            momo_ref_form = MomoRefNumberForm(request.POST, instance=pledge)
            if momo_ref_form.is_valid():
                momo_ref_form.save()
                messages.success(request, 'Pledge Successfully updated with Momo Reference code')
                return redirect('app:history')
        momo_ref_form = MomoRefNumberForm()
        return render(request, 'momo_ref.html', {'momo_ref_form': momo_ref_form})

    return redirect('app:history')

def about_us(request):
    return render(request, 'about_us.html', {})


def contact_us(request):
    if request.method=="POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('app:welcome')
    contact_form = ContactForm()
    return render(request, "contact_us.html", {'contact_form': contact_form,})