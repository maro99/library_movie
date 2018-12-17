from django.shortcuts import render


def user_detail_page(request):
    return render(request,'members/user_detail.html')


def user_info_change_page(request):
    return render(request, 'members/user_info_change.html')