from django.contrib.auth import logout
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
User = get_user_model()


def signout_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
    return redirect('main_page')
