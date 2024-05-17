from django.shortcuts import render
from functions.general import query_result

def page_kelola_user(request):
    user_email = request.COOKIES.get('email')
    
    playlists = query_result(f"""
                        SELECT up.judul, up.jumlah_lagu, up.total_durasi, up.id_user_playlist
                        FROM USERPLAYLIST as up
                        WHERE up.email_pembuat = '{user_email}';
                             """)
    
    context = {
        'playlists': playlists,
    }
    
    return render(request, 'playlist_page.html', context)

def page_user_playlist_detail(request, playlist_id):
    user_email = request.COOKIES.get('email')

    playlist = query_result(f"""
        SELECT up.judul, ak.nama AS pembuat, up.jumlah_lagu, up.total_durasi, up.tanggal_dibuat, up.deskripsi
        FROM USERPLAYLIST AS up
        JOIN AKUN AS ak ON up.email_pembuat = ak.email
        WHERE up.id_user_playlist = '{playlist_id}' AND ak.email = '{user_email}';
    """)

    songs = query_result(f"""
        SELECT k.judul AS song_title, a.nama AS artist_name, s.durasi
        FROM PLAYLISTSONG AS ps
        JOIN SONG AS s ON ps.id_konten = s.id_konten
        JOIN KONTEN AS k ON s.id_konten = k.id
        JOIN ARTIST AS a ON s.id_artist = a.id
        JOIN USERPLAYLIST AS up on up.id_playlist = ps.id_playlist
        WHERE up.id_user_playlist = '{playlist_id}';
    """)

    context = {
        'playlist': playlist[0] if playlist else None,
        'songs': songs,
    }

    return render(request, 'playlist_details.html', context)

def song_details(request, song_id):
    user_email = request.COOKIES.get('email')

    song_details = f"""
        SELECT k.judul AS song_title, g.genre, k.durasi, k.tanggal_rilis, k.tahun,
        s.total_download
        FROM SONG AS s
        JOIN KONTEN AS k ON k.id = s.id_konten
        JOIN GENRE AS g ON k.id = g.id_konten
        WHERE s.id_konten = '{song_id}';
    """
    song = query_result(song_details)

    artist_query = f"""
        SELECT ak.nama as nama_artis
        FROM SONG AS s
        JOIN ARTIST AS a ON s.id_artist = a.id
        JOIN AKUN AS ak ON a.email_akun = ak.email
        WHERE s.id_konten = '{song_id}';
    """
    artist = query_result(artist_query)

    songwriter_query = f"""
        SELECT ak.nama as nama_songwriter
        FROM SONGWRITERWRITESONG AS sws
        JOIN SONGWRITER AS sw ON sws.id_songwriter = sw.id
        JOIN AKUN AS ak ON sw.email_akun = ak.email
        WHERE sws.id_song = '{song_id}';
    """
    songwriter = query_result(songwriter_query)

    album_query = f"""
        SELECT al.judul AS album_title
        FROM SONG AS s
        LEFT JOIN ALBUM AS al ON s.id_album = al.id
        WHERE s.id_konten = '{song_id}';
    """
    album = query_result(album_query)

    user = query_result(f"""
        SELECT akun.email, premium.akun_email
        FROM akun
        LEFT JOIN premium ON akun.email = premium.akun_email
        WHERE akun.email = '{user_email}';
    """)

    is_premium = user[0]['akun_email'] is not None if user else False

    context = {
        'song': song[0] if song else None,
        'artist': artist[0] if artist else None,
        'songwriter': songwriter[0] if songwriter else None,
        'album': album[0] if album else None,
        'is_premium': is_premium,
    }

    return render(request, 'play_song.html', context)