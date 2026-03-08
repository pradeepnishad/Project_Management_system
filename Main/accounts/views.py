from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientSignupForm


def client_signup(request):

    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ClientSignupForm()

    return render(request, 'signup.html', {'form': form})