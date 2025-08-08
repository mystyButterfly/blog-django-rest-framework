from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    users = User.objects.values('username')
    context = {'users': users}
    return render(request, 'home.html', context)