from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

# Create your views here.
@csrf_exempt
def kelola(request):
    email = request.COOKIES['email']
    nama = request.COOKIES['nama']
    nama_album = ""
    list_lagu = []

    with connection.cursor() as cursor:
        cursor.execute('''SELECT AL.id, AL.judul, L.nama, AL.jumlah_lagu, AL.total_durasi 
                       FROM label L, album AL, artist AR, song S
                       WHERE AR.email_akun = %s AND AR.id = S.id_artist AND S.id_album = AL.id
                       AND AL.id_label = L.id
                       UNION
                       (SELECT AL.id, AL.judul, L.nama, AL.jumlah_lagu, AL.total_durasi 
                       FROM label L, album AL, songwriter SW, song S, songwriter_write_song SWS
                       WHERE SW.email_akun = %s AND SW.id = SWS.id_songwriter AND SWS.id_song = S.id_konten
                       AND S.id_album = AL.id AND AL.id_label = L.id)''', [email, email])
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
                        FROM album AL, song S, konten K, artist AR
                        WHERE AR.email_akun = %s AND AR.id = S.id_artist AND S.id_konten = K.id
                        AND S.id_album = AL.id AND AL.id = %s
                        UNION
                        (SELECT K.id, K.judul, K.durasi, S.total_play, S.total_download
                        FROM songwriter SW, songwriter_write_song SWS, song S, konten K, album AL
                        WHERE SW.email_akun = %s AND SW.id = SWS.id_songwriter AND SWS.id_song = S.id_konten
                        AND S.id_konten = K.id AND S.id_album = AL.id AND AL.id = %s)''', [email, id_album, email, id_album])
            list_lagu = cursor.fetchall()
        
    context = {
        'nama' : nama,
        'data_album': data_album,
        'list_lagu': list_lagu,
        'nama_album' : nama_album,
    }

    return render(request, "kelola_album_song.html", context)

@csrf_exempt
def create_album(request):
    nama_pengguna = request.COOKIES['nama']
    with connection.cursor() as cursor:
                cursor.execute('''SELECT L.nama 
                                FROM label L''')
                list_label = cursor.fetchall()
    print(list_label)
    
    roles = request.COOKIES['role']
    role = roles.split(" ")

    email = request.COOKIES['email']

    if ("Artist" in role and "Songwriter" in role):
        print("ini 3")
        with connection.cursor() as cursor:
            cursor.execute('''SELECT A.nama 
                            FROM akun A, songwriter S
                            WHERE S.email_akun = A.email''', [email])
            songwriter = cursor.fetchall()
        
        context = {
            'songwriters' : songwriter ,
            'labels' : list_label,
            'nama_pengguna' : nama_pengguna,
        }


    elif ("Songwriter" in role):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT A.nama 
                            FROM akun A, artist AR
                            WHERE AR.email_akun = A.email''')
            artist = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute('''SELECT A.nama 
                            FROM akun A, songwriter S
                            WHERE S.email_akun = A.email''', [email])
            songwriter = cursor.fetchall()
        
        context = {
            'songwriters' : songwriter ,
            'artists' : artist,
            'labels' : list_label,
            'nama_pengguna' : nama_pengguna
        }    

    elif ("Artist" in role):
        print("ini 2")
        with connection.cursor() as cursor:
            cursor.execute('''SELECT A.nama 
                            FROM akun A, songwriter S
                            WHERE S.email_akun = A.email''')
            songwriter = cursor.fetchall()
        
        context = {
            'songwriters' : songwriter ,
            'labels' : list_label,
            'nama_pengguna' : nama_pengguna
        }
    

    return render(request, "create_album.html", context)

@csrf_exempt
def create_lagu(request):
    if request.method == "POST":
        nama_album = request.POST.get('tambah-lagu')
        nama_pengguna = request.COOKIES['nama']

        roles = request.COOKIES['role']
        role = roles.split(" ")

        email = request.COOKIES['email']

        if ("Songwriter" in role):
            with connection.cursor() as cursor:
                cursor.execute('''SELECT A.nama 
                                FROM akun A, artist AR
                                WHERE AR.email_akun = A.email''')
                artist = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute('''SELECT A.nama 
                                FROM akun A, songwriter S
                                WHERE S.email_akun = A.email''', [email])
                songwriter = cursor.fetchall()
            
            context = {
                'nama_album' : nama_album,
                'nama_pengguna' : nama_pengguna,
                'songwriters' : songwriter ,
                'artists' : artist
            }    

        elif ("Artist" in role):
            with connection.cursor() as cursor:
                cursor.execute('''SELECT A.nama 
                                FROM akun A, songwriter S
                                WHERE S.email_akun = A.email''')
                songwriter = cursor.fetchall()
            
            context = {
                'nama_album' : nama_album,
                'nama_pengguna' : nama_pengguna,
                'songwriters' : songwriter ,
            }    

    return render(request, "create_lagu.html", context)

@csrf_exempt
def delete_lagu(request): # ingetin perlu revisi
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
            cursor.execute('''UPDATE album A
                        SET jumlah_lagu = A.jumlah_lagu - 1, 
                        total_durasi = A.total_durasi - K.durasi
                        FROM song S, konten K
                        WHERE A.id = %s AND A.id = S.id_album AND S.id_konten = K.id AND K.id = %s''', [targeted_id_album, target_lagu])
            
        with connection.cursor() as cursor:
            cursor.execute('''DELETE 
                        FROM konten
                        WHERE id = %s''', [target_lagu])
    
    return render(request, "kelola_album_song.html")

@csrf_exempt
def delete_album(request):
    if request.method == 'POST':
        target_album = request.POST.get('deleted-album')
        print(target_album)

        with connection.cursor() as cursor:
            cursor.execute('''DELETE 
                        FROM album
                        WHERE id = %s''', [target_album])
        
    return render(request, "kelola_album_song.html") 
@csrf_exempt
def tambah_lagu(request):
    if request.method == 'POST':
        album = request.POST.get('album')
        judul = request.POST.get('judul')
        songwriter = request.POST.getlist('options-sw')
        artist = request.POST.get('options-ar')
        genre = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

        print(album)
        print(judul)
        print(songwriter)
        print(artist)
        print(genre)
        print(durasi)

        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id 
                        FROM album
                        WHERE judul = %s''', [album])
            id_album = cursor.fetchone()
        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT AR.id 
                        FROM artist AR, akun AK
                        WHERE AK.nama = %s AND AK.email = AR.email_akun''', [artist])
            id_artist = cursor.fetchone()
        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id
                        FROM konten
                        WHERE id NOT IN (SELECT id_konten FROM podcast) AND
                        id NOT IN (SELECT id_konten FROM song)''')
            id_konten = cursor.fetchone()
        
        if id_konten is None:
            id_konten = str(uuid.uuid4())

            sql_konten = '''INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi)
                            VALUES (%s, %s, NOW(), EXTRACT(YEAR FROM NOW()), %s)'''
            param_konten = [id_konten, judul, int(durasi)]

            with connection.cursor() as cursor:
                cursor.execute(sql_konten, param_konten)

            sql_song = '''INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
                            VALUES (%s, %s, %s, 0, 0)'''
            param_song = [id_konten, id_artist, id_album]

            with connection.cursor() as cursor:
                cursor.execute(sql_song, param_song)
        
        else:
            id_konten = id_konten[0]
            print(id_konten)

            with connection.cursor() as cursor:
                cursor.execute('''UPDATE konten
                               SET judul = %s, 
                               tanggal_rilis = NOW(), 
                               tahun = EXTRACT(YEAR FROM NOW()),
                               durasi = %s,
                               WHERE id = %s''', [judul, int(durasi), id_konten])
            
            sql_song = '''INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
                            VALUES (%s, %s, %s, 0, 0)'''
            param_song = [id_konten, id_artist, id_album]

            with connection.cursor() as cursor:
                cursor.execute(sql_song, param_song)

        sql_sws = '''INSERT INTO songwriter_write_song (id_songwriter, id_song)
                    VALUES (%s, %s)'''
        for sw in songwriter:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT SW.id
                               FROM songwriter SW, akun AK
                               WHERE AK.nama = %s AND AK.email = SW.email_akun''', [sw])
                id_songwriter = cursor.fetchone()

            param_sws = [id_songwriter, id_konten]
            
            with connection.cursor() as cursor:
                cursor.execute(sql_sws, param_sws)
        
        sql_genre = '''INSERT INTO genre (id_konten, genre)
                        VALUES (%s, %s)'''
        
        for g in genre:
            param_genre = [id_konten, g]
            
            with connection.cursor() as cursor:
                cursor.execute(sql_genre, param_genre)
            

    return render(request, "create_lagu.html",)

@csrf_exempt
def tambah_album(request):
    if request.method == 'POST':
        album = request.POST.get('album')
        label = request.POST.get('labels')
        judul = request.POST.get('judul')
        songwriter = request.POST.getlist('options-sw')
        artist = request.POST.get('options-ar')
        genre = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')

        print(album)
        print(label)
        print(judul)
        print(songwriter)
        print(artist)
        print(genre)
        print(durasi)

        with connection.cursor() as cursor:
            cursor.execute('''SELECT AR.id 
                        FROM artist AR, akun AK
                        WHERE AK.nama = %s AND AK.email = AR.email_akun''', [artist])
            id_artist = cursor.fetchone()
        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id 
                        FROM label
                        WHERE nama = %s''', [label])
            id_label = cursor.fetchone()
        
        new_id_album = str(uuid.uuid4())
        
        sql_album = '''INSERT INTO album (id, judul, jumlah_lagu, id_label, total_durasi)
                        VALUES (%s, %s, %s, %s, %s)'''
        param_album = [new_id_album, album, 1, id_label, int(durasi)]

        with connection.cursor() as cursor:
            cursor.execute(sql_album, param_album)
        
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id
                        FROM konten
                        WHERE id NOT IN (SELECT id_konten FROM podcast) AND
                        id NOT IN (SELECT id_konten FROM song)''')
            id_konten = cursor.fetchone()

        if id_konten is None:
            id_konten = str(uuid.uuid4())

            sql_konten = '''INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi)
                            VALUES (%s, %s, NOW(), EXTRACT(YEAR FROM NOW()), %s)'''
            param_konten = [id_konten, judul, int(durasi)]

            with connection.cursor() as cursor:
                cursor.execute(sql_konten, param_konten)

            sql_song = '''INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
                            VALUES (%s, %s, %s, 0, 0)'''
            param_song = [id_konten, id_artist, new_id_album]

            with connection.cursor() as cursor:
                cursor.execute(sql_song, param_song)
        
        else:
            id_konten = id_konten[0]

            with connection.cursor() as cursor:
                cursor.execute('''UPDATE konten
                               SET judul = %s, 
                               tanggal_rilis = NOW(), 
                               tahun = EXTRACT(YEAR FROM NOW()),
                               durasi = %s
                               WHERE id = %s'''
                               , [judul, int(durasi), id_konten])
            
            sql_song = '''INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download)
                            VALUES (%s, %s, %s, 0, 0)'''
            param_song = [id_konten, id_artist, new_id_album]

            with connection.cursor() as cursor:
                cursor.execute(sql_song, param_song)


        sql_sws = '''INSERT INTO songwriter_write_song (id_songwriter, id_song)
                    VALUES (%s, %s)'''
        for sw in songwriter:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT SW.id
                               FROM songwriter SW, akun AK
                               WHERE AK.nama = %s AND AK.email = SW.email_akun''', [sw])
                id_songwriter = cursor.fetchone()

            param_sws = [id_songwriter, id_konten]
            
            with connection.cursor() as cursor:
                cursor.execute(sql_sws, param_sws)
        
        sql_genre = '''INSERT INTO genre (id_konten, genre)
                        VALUES (%s, %s)'''
        
        for g in genre:
            param_genre = [id_konten, g]
            
            with connection.cursor() as cursor:
                cursor.execute(sql_genre, param_genre)
            

    return render(request, "create_album.html",)