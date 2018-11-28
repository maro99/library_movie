from django.contrib.auth import logout
from django.shortcuts import render


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request,'members/login.html')