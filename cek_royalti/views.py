from django.shortcuts import render

# Create your views here.
def cek(request):
    context = {
        'name': 'Ini Halaman Cek Royalti',
    }

    return render(request, "cek_royalti.html", context)