from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Accounts


def home(request):
    return render(request, 'index.html')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f'{user.email} registration successfully')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user=user)
                try:
                    next = request.GET['next']
                    return redirect(next)
                except KeyError:
                    return redirect('home')
            else:
                messages.error(request, 'username or password error')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    messages.success(request, 'user logout successfully')
    return redirect('login')


@login_required(login_url='login')
def userProfile(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def userProfileEdit(request):
    user = Accounts.objects.get(email=request.user)
    if request.method == 'POST':
        try:
            user.first_name = request.POST['first-name']
            user.last_name = request.POST['last-name']
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.photo = request.FILES['photo']
            user.save()
            messages.success(request, 'profile update successfully')
            return redirect('profile')
        except KeyError:
            messages.error(request, 'Please given valid information')
            return redirect('edit-profile')
    else:
        return render(request, 'editprofile.html')
