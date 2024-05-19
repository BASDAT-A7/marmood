from datetime import datetime
from time import timezone
from django.shortcuts import redirect, render
from functions.general import query_result
from django.db import connection
from django.http import HttpResponseRedirect
from .forms import AddPlaylistForm, AddSongForm, AddToPlaylistForm, EditPlaylistForm
import uuid

def generate_unique_id():
    return str(uuid.uuid4())

def page_kelola_user(request):
    user_email = request.COOKIES.get('email')
    
    playlists = query_result(f"""
                        SELECT up.judul, up.jumlah_lagu, up.total_durasi, up.id_user_playlist
                        FROM user_playlist as up
                        WHERE up.email_pembuat = '{user_email}';
                             """)
    
    context = {
        'playlists': playlists,
    }
    
    return render(request, 'playlist_page.html', context)

def add_playlist(request):
    if request.method == 'POST':
        form = AddPlaylistForm(request.POST)
        if form.is_valid():
            judul_playlist = form.cleaned_data['judul_playlist']
            description = form.cleaned_data['description']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO playlist (judul) VALUES (%s)", [judul_playlist])
                playlist_id = generate_unique_id()

            tanggal_dibuat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            jumlah_lagu = 0
            total_duration = 0
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_playlist (email, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [request.user.email, generate_unique_id(), judul_playlist, description, jumlah_lagu, tanggal_dibuat, playlist_id, total_duration])

            return redirect('kelola-user')

    else:
        form = AddPlaylistForm()

    playlists = query_result(f"""
        SELECT up.judul, up.jumlah_lagu, up.total_durasi, up.id_user_playlist
        FROM user_playlist as up
        WHERE up.email_pembuat = '{request.user.email}';
    """)
    
    context = {
        'playlists': playlists,
        'form': form
    }

    return render(request, 'playlist_page.html', context)

def page_user_playlist_detail(request, playlist_id):
    user_email = request.COOKIES.get('email')

    playlist = query_result(f"""
        SELECT up.judul, ak.nama AS pembuat, up.jumlah_lagu, up.total_durasi, up.tanggal_dibuat, up.deskripsi, up.id_user_playlist
        FROM user_playlist AS up
        JOIN akun AS ak ON up.email_pembuat = ak.email
        WHERE up.id_user_playlist = '{playlist_id}' AND ak.email = '{user_email}';
    """)

    songs = query_result(f"""
        SELECT k.judul AS song_title, a.nama AS artist_name, s.durasi, s.id_konten as id
        FROM playlist_song AS ps
        JOIN song AS s ON ps.id_konten = s.id_konten
        JOIN konten AS k ON s.id_konten = k.id
        JOIN artist AS a ON s.id_artist = a.id
        JOIN user_playlist AS up on up.id_playlist = ps.id_playlist
        WHERE up.id_user_playlist = '{playlist_id}';
    """)

    context = {
        'playlist': playlist[0] if playlist else None,
        'songs': songs,
    }

    return render(request, 'playlist_details.html', context)

def add_song(request, playlist_id):
    if request.method == 'POST':
        form = AddSongForm(request.POST)
        if form.is_valid():
            song_artist = form.cleaned_data['song_artist']
            song_title, artist_name = song_artist.split(' - ')

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM konten 
                    WHERE judul = %s AND artist = %s
                """, [song_title, artist_name])
                row = cursor.fetchone()
                if row:
                    song_id = row[0]
                    
                    playlist_id = request.GET.get('playlist_id')
                    
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO playlist_song (song_id, playlist_id)
                            VALUES (%s, %s)
                        """, [song_id, playlist_id])
                    
                    return redirect('playlist-details', playlist_id=playlist_id)
    else:
        form = AddSongForm()

    return render(request, 'playlist_details.html', {'form': form})

def song_details(request, song_id):
    user_email = request.COOKIES.get('email')

    song_details = f"""
        SELECT k.judul AS song_title, g.genre, k.durasi, k.tanggal_rilis, k.tahun,
        s.total_download
        FROM song AS s
        JOIN konten AS k ON k.id = s.id_konten
        JOIN genre AS g ON k.id = g.id_konten
        WHERE s.id_konten = '{song_id}';
    """
    song = query_result(song_details)

    artist_query = f"""
        SELECT ak.nama as nama_artis
        FROM song AS s
        JOIN artist AS a ON s.id_artist = a.id
        JOIN akun AS ak ON a.email_akun = ak.email
        WHERE s.id_konten = '{song_id}';
    """
    artist = query_result(artist_query)

    songwriter_query = f"""
        SELECT ak.nama as nama_songwriter
        FROM songwriter_write_song AS sws
        JOIN songwriter AS sw ON sws.id_songwriter = sw.id
        JOIN akun AS ak ON sw.email_akun = ak.email
        WHERE sws.id_song = '{song_id}';
    """
    songwriter = query_result(songwriter_query)

    album_query = f"""
        SELECT al.judul AS album_title
        FROM song AS s
        LEFT JOIN album AS al ON s.id_album = al.id
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
        'is_premium': is_premium
    }

    return render(request, 'play_song.html', context)

def add_song_to_playlist(request):
    user_email = request.COOKIES.get('email')
    song_title = request.POST.get('song_title')
    artist_name = request.POST.get('artist_name')
    success = False
    message = ""

    if request.method == 'POST':
        form = AddToPlaylistForm(request.POST)
        if form.is_valid():
            playlist_id = form.cleaned_data['playlist_id']
            song_title = form.cleaned_data['song_title']
            artist_name = form.cleaned_data['artist_name']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT k.id
                    FROM konten AS k
                    JOIN song AS s ON s.id_konten = k.id
                    JOIN artist AS a ON s.id_artist = a.id
                    JOIN akun AS ak ON a.email_akun = ak.email
                    WHERE k.judul = %s AND ak.nama = %s
                """, [song_title, artist_name])
                row = cursor.fetchone()
                if row:
                    song_id = row[0]

                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM playlist_song
                        WHERE id_song = %s AND id_playlist = %s
                    """, [song_id, playlist_id])
                    song_in_playlist = cursor.fetchone()[0] > 0

                    if song_in_playlist:
                        message = f"Lagu '{song_title}' sudah ada di playlist."
                    else:
                        cursor.execute("""
                            INSERT INTO playlist_song (id_song, id_playlist)
                            VALUES (%s, %s)
                        """, [song_id, playlist_id])
                        message = f"Lagu '{song_title}' berhasil ditambahkan ke playlist."
                        success = True

            context = {'message': message, 'success': success, 'playlist_id': playlist_id}
            return render(request, 'play_song.html', context)

    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, judul FROM user_playlist
                WHERE user_email = %s
            """, [user_email])
            playlists = cursor.fetchall()

        form = AddToPlaylistForm(initial={'song_title': song_title, 'artist_name': artist_name})
        form.fields['playlist_id'].choices = [(playlist[0], playlist[1]) for playlist in playlists]

        context = {
            'form': form,
            'song': {'song_title': song_title}, 
            'artist': {'nama_artis': artist_name},
            'success': success,
            'message': message
        }
        return render(request, 'play_song.html', context)

def edit_playlist(request, playlist_id):
    if request.method == 'POST':
        form = EditPlaylistForm(request.POST)
        if form.is_valid():
            judul_playlist = form.cleaned_data['judul_playlist']
            deskripsi_playlist = form.cleaned_data['deskripsi_playlist']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user_playlist
                    SET judul = %s, deskripsi = %s
                    WHERE id_user_playlist = %s
                """, [judul_playlist, deskripsi_playlist, playlist_id])
                
            return redirect('', playlist_id=playlist_id)
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT judul, deskripsi
                FROM user_playlist
                WHERE id_user_playlist = %s
            """, [playlist_id])
            playlist_data = cursor.fetchone()
            
        if playlist_data:
            initial_data = {'judul_playlist': playlist_data[0], 'deskripsi_playlist': playlist_data[1]}
            form = EditPlaylistForm(initial=initial_data)
        else:
            form = EditPlaylistForm()

    return render(request, 'playlist_page.html', {'form': form, 'playlist_id': playlist_id})

def delete_song_from_playlist(request, playlist_id, song_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM playlist_song WHERE id_playlist = %s AND id_song = %s", [playlist_id, song_id])
    
    return redirect('playlist-details', playlist_id=playlist_id)

def download_song(request, song_id):
    user_email = user_email = request.COOKIES.get('email')

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM downloaded_song WHERE id_song = %s AND email_downloader = %s", [song_id, user_email])
        song_already_downloaded = cursor.fetchone()[0] > 0

        cursor.execute("SELECT judul FROM konten WHERE id = %s", [song_id])
        song_name = cursor.fetchone()[0]

    if song_already_downloaded:
        message = f"Lagu dengan judul '{song_name}' sudah pernah diunduh."
        song_downloaded = True
    else:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO downloaded_song (id_song, email_downloader) VALUES (%s, %s)", [song_id, user_email])
            
        message = f"Lagu '{song_name}' berhasil diunduh."
        song_downloaded = False

    return render(request, 'play_song.html', {'message': message, 'song_downloaded': song_downloaded})

def shuffle_play(request, playlist_id):
    user_email = request.COOKIES.get('email')
    if not user_email:
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ps.id_song
            FROM user_playlist AS up
            JOIN playlist_song AS ps ON up.id_playlist = ps.id_playlist
            WHERE up.user_id_playlist = %s
        """, [playlist_id])
        songs = cursor.fetchall()

    if not songs:
        return redirect('playlist-details', playlist_id = playlist_id)

    song_ids = [song[0] for song in songs]

    now = timezone.now()

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu)
            VALUES (%s, %s, %s, %s)
        """, [user_email, playlist_id, user_email, now])

    with connection.cursor() as cursor:
        for song_id in song_ids:
            cursor.execute("""
                INSERT INTO akun_play_song (email_pemain, id_song, waktu)
                VALUES (%s, %s, %s)
            """, [user_email, song_id, now])

    return redirect('playlist-details', playlist_id = playlist_id)

def play_lagu(request, song_id):
    if request.method == 'POST':
        song_progress = int(request.POST.get('song_progress', 0))

    if song_progress > 70:
        user_email = request.COOKIES.get('email')
        if user_email:
            now = timezone.now()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO akun_play_song (email_pemain, id_song, waktu)
                    VALUES (%s, %s, %s)
                """, [user_email, song_id, now])
                
    return redirect('play-song', song_id=song_id)