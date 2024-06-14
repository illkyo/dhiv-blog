from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

class Profile(View):
    
    reg_form = RegisterForm()
    login_form = LoginForm()
    
    context = {
            'reg_form': reg_form,
            'login_form': login_form,
        }
    
    def get(self, request):
        return render(request, 'users/profile.html', self.context)
    
    def post(self, request):
        if request.POST.get('submit') == 'sign_up':
            reg_form_fill = RegisterForm(request.POST)
            
            reg_context = {
                'reg_form': reg_form_fill,
                'login_form': self.login_form,
            }

            if reg_form_fill.is_valid():
                reg_form_fill.save()
                username = reg_form_fill.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!. Now you can Log In')
                return redirect('users-profilepage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                return render(request, 'users/profile.html', reg_context)
                
        if request.POST.get('submit') == 'log_in':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('users-profilepage')
            else:
                messages.warning(request, f'Invalid Login')
                return redirect('users-profilepage')
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('users-profilepage')