from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View

class Profile(View):
    
    def get(self, request):
        return render(request, 'users/profile.html')

    def post(self, request):
        
        if request.POST.get('submit') == 'log_out':
            logout(request)
            return redirect('blog-homepage')