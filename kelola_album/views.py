from django.shortcuts import render
from django.db import connection

# Create your views here.
def kelola_album(request):
    email = request.COOKIES['email']
    nama = request.COOKIES['nama']
    nama_album = ""
    list_lagu = []

    with connection.cursor() as cursor:
        cursor.execute('''SELECT A.id, A.judul, A.jumlah_lagu, A.total_durasi 
                       FROM label L, album A
                       WHERE L.email = %s AND L.id = A.id_label''', [email])
        data_album = cursor.fetchall()
    
    # print(data_album)
    if request.method == 'POST':
        id_album = request.POST.get('list-lagu')
        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT judul 
                        FROM album
                        WHERE id = %s''', [id_album])
            nama_album = cursor.fetchone()

        with connection.cursor() as cursor:
            cursor.execute('''SELECT K.id, K.judul, K.durasi, S.total_play, S.total_download 
                        FROM album A, song S, konten K
                        WHERE A.id = %s AND A.id = S.id_album AND S.id_konten = K.id''', [id_album])
            list_lagu = cursor.fetchall()
        
    context = {
        'nama' : nama,
        'data_album': data_album,
        'list_lagu': list_lagu,
        'nama_album' : nama_album,
    }

    return render(request, "kelola_album.html", context)

def delete_album(request):
    if request.method == 'POST':
        target_album = request.POST.get('deleted-album')
        print(target_album)

        with connection.cursor() as cursor:
            cursor.execute('''DELETE 
                        FROM album
                        WHERE id = %s''', [target_album])
        
    return render(request, "kelola_album.html")

def delete_lagu(request):
    if request.method == 'POST':
        target_lagu = request.POST.get('deleted-lagu')
        print(target_lagu)

        with connection.cursor() as cursor:
            cursor.execute(''' SELECT A.id
                        FROM album A, song S
                        WHERE S.id_konten = %s AND S.id_album = A.id''', [target_lagu])
            targeted_id_album = cursor.fetchone()[0]
            print(targeted_id_album)

        with connection.cursor() as cursor:
            cursor.execute('''DELETE 
                        FROM konten
                        WHERE id = %s''', [target_lagu])
        

    return render(request, "kelola_album.html")