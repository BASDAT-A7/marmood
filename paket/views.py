from django.shortcuts import render

def show_paket(request):
    return render(request, "paket.html")