from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from blog.models import Post
from .forms import UserUpdateForm, ProfileUpdateForm, LoginForm, RegisterForm
from blog.views import AuthModalMixin

class Profile(LoginRequiredMixin, View):
    
    def get(self, request):
        
        user_posts = Post.objects.filter(author=self.request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
        prof_context = {
            'user_posts': user_posts,
            'u_form': u_form,
            'p_form': p_form,
        }
        
        return render(request, 'users/profile.html', prof_context)

    def post(self, request):
        
        if request.POST.get('submit') == 'change_prof':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('users-profilepage')
            
            redirect('users-profilepage')
            
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('blog-homepage')
        
class Login(AuthModalMixin, View):

    template_name = 'users/login.html'
    view_name = 'users-login'

    reg_form = RegisterForm()
    login_form = LoginForm()
    
    def get(self, request):

        context = {
            'reg_form': self.reg_form,
            'login_form': self.login_form,
        }

        return render(request, self.template_name, context)
    
class PostCreate(LoginRequiredMixin, CreateView):

    template_name = 'users/post_form.html'
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/post_form.html'
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
# class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

#     model = Post

#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False