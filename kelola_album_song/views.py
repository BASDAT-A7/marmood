from django.shortcuts import render

# Create your views here.
def kelola(request):
    context = {
        'name': 'Ini Halaman Kelola Album dan Song',
    }

    return render(request, "kelola_album_song.html", context)

def create_album(request):
    context = {}
    return render(request, "create_album.html", context)

def create_lagu(request):
    context = {}
    return render(request, "create_lagu.html", context)