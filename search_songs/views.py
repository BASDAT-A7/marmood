from django.shortcuts import render
from functions.general import query_result

def search_songs(request):
    dicari = request.POST.get('q')
    search_songs = query_result(f"""
        SELECT 'SONG' AS Type, K.id AS id_konten, K.judul, A.nama AS Oleh
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        JOIN ARTIST Ar ON S.id_artist = Ar.id
        JOIN AKUN A ON Ar.email_akun = A.email
        WHERE K.judul ILIKE %s

        UNION ALL

        SELECT 'PODCAST' AS Type, id_konten AS id_konten, K.judul, A.nama AS Oleh
        FROM PODCAST P
        JOIN KONTEN K ON P.id_konten = K.id
        JOIN PODCASTER Pr ON P.email_podcaster = Pr.email
        JOIN AKUN A ON Pr.email = A.email
        WHERE K.judul ILIKE %s

        UNION ALL

        SELECT 'USER PLAYLIST' AS Type, id_user_playlist AS id_konten , UP.judul, A.nama AS Oleh
        FROM USER_PLAYLIST UP
        JOIN AKUN A ON UP.email_pembuat = A.email
        WHERE UP.judul ILIKE %s
    """, (f'%{dicari}%', f'%{dicari}%', f'%{dicari}%'))


    # Mulai dari line ini, harusnya masuk ke tombol download di detail lagu:
    roles = request.COOKIES['role']
    list_role = roles.split(" ")
     
    context = {
        'dicari': dicari,
        'search_songs': search_songs,
        'list_role': list_role,
    }
    print("ini searchsongs: ", search_songs)
    return render(request, 'search_songs.html', context)