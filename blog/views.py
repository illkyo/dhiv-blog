from django.shortcuts import render, redirect
from .models import Post
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

class Home(View):
    
    posts =  Post.objects.all()
    reg_form = RegisterForm()
    login_form = LoginForm()
    
    context = {
            'posts': posts,
            'reg_form': reg_form,
            'login_form': login_form,
        }
    
    def get(self, request):
        return render(request, 'blog/home.html', self.context)
    
    def post(self, request):
        if request.POST.get('submit') == 'sign_up':
            reg_form_fill = RegisterForm(request.POST)
            
            reg_context = {
                'posts': self.posts,
                'reg_form': reg_form_fill,
                'login_form': self.login_form,
            }

            if reg_form_fill.is_valid():
                reg_form_fill.save()
                username = reg_form_fill.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!. Now you can Log In')
                return redirect('blog-homepage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                return render(request, 'blog/home.html', reg_context)
                
        if request.POST.get('submit') == 'log_in':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('blog-homepage')
            else:
                messages.warning(request, f'Invalid Login')
                return redirect('blog-homepage')
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('blog-homepage')
        
class About(View):
    
    reg_form = RegisterForm()
    login_form = LoginForm()
    
    context = {
            'reg_form': reg_form,
            'login_form': login_form,
        }
    
    def get(self, request):
        return render(request, 'blog/about.html', self.context)
    
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
                return redirect('blog-aboutpage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                return render(request, 'blog/about.html', reg_context)
                
        if request.POST.get('submit') == 'log_in':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('blog-aboutpage')
            else:
                messages.warning(request, f'Invalid Login')
                return redirect('blog-aboutpage')
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('blog-aboutpage')

class Profile(View):
    
    reg_form = RegisterForm()
    login_form = LoginForm()
    
    context = {
            'reg_form': reg_form,
            'login_form': login_form,
        }
    
    def get(self, request):
        return render(request, 'blog/profile.html', self.context)
    
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
                return redirect('blog-profilepage')
            else:
                messages.warning(request, f'Account was not created. Please try again')
                return render(request, 'blog/profile.html', reg_context)
                
        if request.POST.get('submit') == 'log_in':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('blog-profilepage')
            else:
                messages.warning(request, f'Invalid Login')
                return redirect('blog-profilepage')
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('blog-profilepage')

        
# class All(View):
    
#     reg_form = RegisterForm()
#     login_form = LoginForm()
#     template_name = " "
#     redirect_name = " "
    
#     context = {
#             'reg_form': reg_form,
#             'login_form': login_form,
#         }
    
#     def get(self, request):
#         return render(request, self.template_name, self.context)
    
#     def post(self, request):
#         if request.POST.get('submit') == 'sign_up':
#             reg_form_fill = RegisterForm(request.POST)
            
#             reg_context = {
#                 'reg_form': reg_form_fill,
#                 'login_form': self.login_form,
#             }

#             if reg_form_fill.is_valid():
#                 reg_form_fill.save()
#                 username = reg_form_fill.cleaned_data.get('username')
#                 messages.success(request, f'Account created for {username}!. Now you can Log In')
#                 return redirect(self.redirect_name)
#             else:
#                 messages.warning(request, f'Account was not created. Please try again')
#                 return render(request, 'blog/home.html', reg_context)
                
#         if request.POST.get('submit') == 'log_in':
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('blog-homepage')
#             else:
#                 messages.warning(request, f'Invalid Login')
#                 return redirect('blog-homepage')
                
#         if request.POST.get('submit') == 'log_out':
#             logout(request)
#             return redirect('blog-homepage')


# def home(request):
#     if request.method == 'POST':
#         if request.POST.get('submit') == 'sign_up':
#             login_form = LoginForm()
#             reg_form = RegisterForm(request.POST)
#             if reg_form.is_valid():
#                 reg_form.save()
#                 username = reg_form.cleaned_data.get('username')
#                 messages.success(request, f'Account created for {username}!. Now you can Log In')
#                 return redirect('blog-homepage')
#             else:
#                 messages.warning(request, f'Account was not created. Please try again')
                
#         if request.POST.get('submit') == 'log_in':
#             reg_form = RegisterForm()
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 login_form = LoginForm()
#                 return redirect('blog-homepage')
#             else:
#                 login_form = LoginForm()
#                 messages.warning(request, f'Invalid Login')
                
#         if request.POST.get('submit') == 'log_out':
#             logout(request)
#             reg_form = RegisterForm()
#             login_form = LoginForm()
#             return redirect('blog-homepage')
#     else:
#         reg_form = RegisterForm()
#         login_form = LoginForm()
        
#     context = {
#         'posts': Post.objects.all(),
#         'reg_form': reg_form,
#         'login_form': login_form,
#     }
#     return render(request, 'blog/home.html', context)

# def about(request):
#     if request.method == 'POST':
#         if request.POST.get('submit') == 'sign_up':
#             reg_form = RegisterForm(request.POST)
#             login_form = LoginForm()
#             if reg_form.is_valid():
#                 reg_form.save()
#                 username = reg_form.cleaned_data.get('username')
#                 messages.success(request, f'Account created for {username}!')
#                 return redirect('blog-homepage')
#             else:
#                 messages.warning(request, f'Account was not created. Please try again')
                
#         if request.POST.get('submit') == 'log_in':
#             reg_form = RegisterForm()
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 login_form = LoginForm()
#                 return redirect('blog-homepage')
#             else:
#                 login_form = LoginForm()
#                 messages.warning(request, f'Invalid Login')
                
#         if request.POST.get('submit') == 'log_out':
#             logout(request)
#             reg_form = RegisterForm()
#             login_form = LoginForm()
#             return redirect('blog-homepage')
#     else:
#         reg_form = RegisterForm()
#         login_form = LoginForm()
        
#     context = {
#         'reg_form': reg_form,
#         'login_form': login_form,
#     }
    
#     return render(request, 'blog/about.html', context)