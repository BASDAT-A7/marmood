from django.shortcuts import render

# Create your views here.
def kelola_album(request):
    context = {
        'name': 'Ini Halaman Kelola Album',
    }

    return render(request, "kelola_album.html", context)