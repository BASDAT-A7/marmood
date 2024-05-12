from django.shortcuts import render

def show_downloaded(request):
    return render(request, "downloaded.html")

def show_deleted(request):
    return render(request, "deleted.html")