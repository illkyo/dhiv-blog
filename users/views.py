from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from blog.models import Post
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

class Profile(LoginRequiredMixin, View):
    
    # posts =  Post.objects.all()
    
    # context= {
    #     'posts': posts
    # }
    
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