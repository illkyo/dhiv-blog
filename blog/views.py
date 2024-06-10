from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'sign_up':
            login_form = AuthenticationForm()
            reg_form = UserCreationForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                username = reg_form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!. Now you can Log In')
                return redirect('blog-homepage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                
        if request.POST.get('submit') == 'log_in':
            reg_form = UserCreationForm()
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                login_form = AuthenticationForm()
                return redirect('blog-homepage')
            else:
                login_form = AuthenticationForm()
                messages.warning(request, f'Invalid Login')
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            reg_form = UserCreationForm()
            login_form = AuthenticationForm()
            return redirect('blog-homepage')
    else:
        reg_form = UserCreationForm()
        login_form = AuthenticationForm()
        
    context = {
        'posts': Post.objects.all(),
        'reg_form': reg_form,
        'login_form': login_form,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'sign_up':
            reg_form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if reg_form.is_valid():
                reg_form.save()
                username = reg_form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('blog-homepage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                
        if request.POST.get('submit') == 'log_in':
            reg_form = UserCreationForm()
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                login_form = AuthenticationForm()
                return redirect('blog-homepage')
            else:
                login_form = AuthenticationForm()
                messages.warning(request, f'Invalid Login')
    else:
        reg_form = UserCreationForm()
        login_form = AuthenticationForm()
        
    context = {
        'reg_form': reg_form,
        'login_form': login_form,
    }
    
    return render(request, 'blog/about.html', context)