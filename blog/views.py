from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post
from users.forms import RegisterForm, LoginForm, CommentCreateForm
from users.models import User

# Kind of a mess right now will fix it up better later
class AuthModalMixin:

    reg_form = RegisterForm()
    login_form = LoginForm()
    
    def post(self, request, *args, **kwargs):

        if self.view_name == 'users-login':
            self.view_name = 'blog-homepage'
            
        if type(self).__name__ == 'Home':
            posts = Post.objects.all()
        else:
            posts = None

        if type(self).__name__ == 'PostDetail':
            post_detail = self.get_object()
            pk = self.kwargs.get('pk')
        else:
            post_detail = None
            pk = None
            
        if type(self).__name__ == 'ViewProfile':
            view_username = self.kwargs.get('username')
            view_user = get_object_or_404(User, username=view_username)
            user_posts = Post.objects.filter(author=view_user)
        else:
            view_username = None
            view_user = None
            user_posts = None

        if request.POST.get('submit') == 'sign_up':
            reg_form_fill = RegisterForm(request.POST)
    
            reg_context = {
                'reg_form': reg_form_fill,
                'login_form': self.login_form,
            }

            if post_detail:
                reg_context.update({'post': post_detail})
                kwargs = {'pk': pk}

            if posts:
                reg_context.update({'posts': posts})
                
            if type(self).__name__ == 'ViewProfile':
                reg_context.update({
                    'view_user' : view_user,
                    'user_posts': user_posts,
                                    })

            if reg_form_fill.is_valid():
                reg_form_fill.save()
                username = reg_form_fill.cleaned_data.get('username')
                messages.success(request, f'އައް އެކައުންޓެއް ހެދިއްޖެ. ލޮގްއިން ވެލައްވާ {username}')
                url = reverse(self.view_name, kwargs=kwargs if kwargs else {})
                return redirect(url)
            else:
                messages.warning(request, f'އެކައުންޓެއް ނުހެދުން. އަލުން ރެޖިސްޓާ ކޮއްލަވާ')
                return render(request, self.template_name, reg_context)
                
        if request.POST.get('submit') == 'log_in':
            login_form_fill = LoginForm(request.POST)
            
            login_context = {
                'reg_form': self.reg_form,
                'login_form': login_form_fill,
            }

            if post_detail:
                login_context.update({'post': post_detail})
                kwargs = {'pk': pk}

            if posts:
                login_context.update({'posts': posts})
                
            if type(self).__name__ == 'ViewProfile':
                login_context.update({
                    'view_user' : view_user,
                    'user_posts': user_posts,
                                    })
                kwargs = {'username': view_username}

            username = request.POST["username"]
            password = request.POST["password"]
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'ލޮގްއިން ވެވިއްޖެ')
                url = reverse(self.view_name, kwargs=kwargs if kwargs else {})
                return redirect(url)
            else:
                messages.warning(request, f'ލޮގްއިން ރަނގަޅެއްނޫން')
                return render(request, self.template_name, login_context)
                
        if request.POST.get('submit') == 'log_out':
            logout(request)
            url = reverse(self.view_name, kwargs=kwargs if kwargs else {})
            return redirect(url)
        
        if request.POST.get('submit') == 'post_delete':
            post = Post.objects.get(pk=pk)
            post.delete()
            return redirect('blog-homepage')
        
        if request.POST.get('submit') == 'comment':
            post = Post.objects.get(pk=pk)
            comment_form_fill = CommentCreateForm(request.POST)
            if comment_form_fill.is_valid():
                comment = comment_form_fill.save(commit=False)
                comment.author = request.user
                comment.post = post            
                comment.save()
                return redirect('blog-postdetail', pk=pk)


class Home(AuthModalMixin, ListView):
    
    model = Post
    template_name = 'blog/home.html'
    view_name = 'blog-homepage'
    context_object_name = 'posts'
    paginate_by = 5
    # ordering = ['-date_posted']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reg_form"] = self.reg_form
        context["login_form"] = self.login_form
        return context
    
    #     reg_form = RegisterForm()
    #     login_form = LoginForm()


    #     if request.POST.get('submit') == 'sign_up':
    #         reg_form_fill = RegisterForm(request.POST)

    #         reg_context = {
    #             'posts' :  posts,
    #             'reg_form': reg_form_fill,
    #             'login_form': login_form,
    #         }

    #         if reg_form_fill.is_valid():
    #             reg_form_fill.save()
    #             username = reg_form_fill.cleaned_data.get('username')
    #             messages.success(request, f'Account created for {username}!. Now you can Log In')
    #             return redirect(self.template_name)
    #         else:
    #             messages.warning(request, f'')
    #             return render(request, self.template_name, reg_context)
                
    #     if request.POST.get('submit') == 'log_in':
    #         login_form_fill = LoginForm(request.POST)
            
    #         login_context = {
    #             'posts' :  Post.objects.all(),
    #             'reg_form': reg_form,
    #             'login_form': login_form_fill,
    #         }

    #         username = request.POST["username"]
    #         password = request.POST["password"]
            
    #         user = authenticate(request, username=username, password=password)
            
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, f'ލޮގްއިން ވެވިއްޖެ')
    #             return redirect('blog-homepage')
    #         else:
    #             messages.warning(request, f'Invalid Login')
    #             return render(request, self.template_name, login_context)
                
    #     if request.POST.get('submit') == 'log_out':
    #         logout(request)
    #         return redirect('blog-homepage')
        
class About(AuthModalMixin, View):
    
    template_name = 'blog/about.html'
    view_name = 'blog-aboutpage'

    def get(self, request):

        context = {
            'reg_form': self.reg_form,
            'login_form': self.login_form,
        }
        return render(request, self.template_name, context)
    
    # def post(self, request):
    #     if request.POST.get('submit') == 'sign_up':
    #         reg_form_fill = RegisterForm(request.POST)
            
    #         reg_context = {
    #             'reg_form': reg_form_fill,
    #             'login_form': self.login_form,
    #         }

    #         if reg_form_fill.is_valid():
    #             reg_form_fill.save()
    #             username = reg_form_fill.cleaned_data.get('username')
    #             messages.success(request, f'Account created for {username}!. Now you can Log In')
    #             return redirect('blog-aboutpage')
    #         else:
    #             messages.warning(request, f'Account was not created. Please try again')
    #             return render(request, self.template_name, reg_context)
                
    #     if request.POST.get('submit') == 'log_in':
    #         username = request.POST["username"]
    #         password = request.POST["password"]
    #         user = authenticate(request, username=username, password=password)
            
    #         if user is not None:
    #             login(request, user)
    #             return redirect('blog-aboutpage')
    #         else:
    #             messages.warning(request, f'Invalid Login')
    #             return redirect('blog-aboutpage')
                
    #     if request.POST.get('submit') == 'log_out':
    #         logout(request)
    #         return redirect('blog-aboutpage')

class PostDetail(AuthModalMixin, DetailView):

    model = Post
    template_name = 'blog/post_detail.html'
    view_name = 'blog-postdetail'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reg_form"] = self.reg_form
        context["login_form"] = self.login_form
        context["comment_form"] = CommentCreateForm()
        return context

class ViewProfile(AuthModalMixin, View):
    
    template_name = 'blog/view_profile.html'
    view_name = 'blog-viewprofile'
    
    def get(self, request, *args, **kwargs):
        
        view_username = self.kwargs.get('username')
        view_user = get_object_or_404(User, username=view_username)
        user_posts = Post.objects.filter(author=view_user)
        
        context = {
            'view_user' : view_user,
            'user_posts': user_posts,
            'reg_form': self.reg_form,
            'login_form': self.login_form,
        }
        
        return render(request, self.template_name, context)
    # def post(self, request, *args, **kwargs):
    #     detail_object = self.get_object()
    #     pk = self.kwargs.get('pk')
    #     reg_form = RegisterForm()
    #     login_form = LoginForm()

    #     if request.POST.get('submit') == 'sign_up':
    #         reg_form_fill = RegisterForm(request.POST)

    #         reg_context = {
    #             'reg_form': reg_form_fill,
    #             'login_form': login_form,
    #             'object': detail_object,
    #         }

    #         if reg_form_fill.is_valid():
    #             reg_form_fill.save()
    #             username = reg_form_fill.cleaned_data.get('username')
    #             messages.success(request, f'އައް އެކައުންޓެއް ހެދިއްޖެ. ލޮގްއިން ވެލައްވާ {username}')
    #             return redirect(self.view_name, pk=pk)
    #         else:
    #             messages.warning(request, f'އެކައުންޓެއް ނުހެދުން. އަލުން ރެޖިސްޓާ ކޮއްލަވާ')
    #             return render(request, self.template_name, reg_context)
                
    #     if request.POST.get('submit') == 'log_in':
    #         login_form_fill = LoginForm(request.POST)
            
    #         login_context = {
    #             'reg_form': reg_form,
    #             'login_form': login_form_fill,
    #             'object': detail_object,
    #         }

    #         username = request.POST["username"]
    #         password = request.POST["password"]
            
    #         user = authenticate(request, username=username, password=password)
            
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, f'ލޮގްއިން ވެވިއްޖެ')
    #             return redirect(self.view_name, pk=pk)
    #         else:
    #             messages.warning(request, f'ލޮގްއިން ރަނގަޅެއްނޫން')
    #             return render(request, self.template_name, login_context)
            
    #     if request.POST.get('submit') == 'log_out':
    #         logout(request)
    #         return redirect(self.view_name, pk=pk)

# class Home(View):
    
#     template_name = 'blog/home.html'
#     posts =  Post.objects.all()
#     reg_form = RegisterForm()
#     login_form = LoginForm()
    
#     context = {
#             'posts': posts,
#             'reg_form': reg_form,
#             'login_form': login_form,
#         }
    
#     def get(self, request):
#         return render(request, self.template_name, self.context)
    
#     def post(self, request):
#         if request.POST.get('submit') == 'sign_up':
#             reg_form_fill = RegisterForm(request.POST)
            
#             reg_context = {
#                 'posts': self.posts,
#                 'reg_form': reg_form_fill,
#                 'login_form': self.login_form,
#             }

#             if reg_form_fill.is_valid():
#                 reg_form_fill.save()
#                 username = reg_form_fill.cleaned_data.get('username')
#                 messages.success(request, f'Account created for {username}!. Now you can Log In')
#                 return redirect('blog-homepage')
#             else:
#                 messages.warning(request, f'Account was not created. Please try again')
#                 return render(request, self.template_name, reg_context)
                
#         if request.POST.get('submit') == 'log_in':
#             login_form_fill = LoginForm(request.POST)
            
#             login_context = {
#                 'posts': self.posts,
#                 'reg_form': self.reg_form,
#                 'login_form': login_form_fill,
#             }
            
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'ލޮގް އިން ވެވިއްޖެ')
#                 return redirect('blog-homepage')
#             else:
#                 messages.warning(request, f'Invalid Login')
#                 return render(request, self.template_name, login_context)
                
#         if request.POST.get('submit') == 'log_out':
#             logout(request)
#             return redirect('blog-homepage')


# class Profile(View):
    
#     reg_form = RegisterForm()
#     login_form = LoginForm()
    
#     context = {
#             'reg_form': reg_form,
#             'login_form': login_form,
#         }
    
#     def get(self, request):
#         return render(request, 'users/profile.html', self.context)
    
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
#                 return redirect('users-profilepage')
#             else:
#                 messages.warning(request, f'Account was not created. Please try again')
#                 return render(request, 'users/profile.html', reg_context)
                
#         if request.POST.get('submit') == 'log_in':
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('users-profilepage')
#             else:
#                 messages.warning(request, f'Invalid Login')
#                 return redirect('users-profilepage')
                
#         if request.POST.get('submit') == 'log_out':
#             logout(request)
#             return redirect('users-profilepage')
        
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