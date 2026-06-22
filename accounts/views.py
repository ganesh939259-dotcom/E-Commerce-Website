from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            return redirect('accounts:login')

        else:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

    return render(request, 'register.html')


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('store:home')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('accounts:login')