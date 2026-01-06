from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

def login_view(request):
    """
    Handles user authentication and role-based redirection.
    """
    print("Login Done")
    if request.user.is_authenticated:
        return redirect('dashboard:router')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(username)
        if user is not None:
            login(request, user)
            return redirect('dashboard:router')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
