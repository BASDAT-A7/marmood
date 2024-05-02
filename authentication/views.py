from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def show_register(request):
    return render(request, "register.html")

def show_register_pengguna(request):
    return render(request, "registerPengguna.html")

def show_register_label(request):
    return render(request, "registerLabel.html")