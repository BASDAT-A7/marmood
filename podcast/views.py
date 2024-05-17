from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
import uuid

# Create your views here.
def query_result(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description is None:
            return []

        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        data = []
        for row in results:
            data.append(dict(zip(columns, row))) 
        return data


def show_detail_podcast(request, podcast_id):
    podcast = query_result("""
        SELECT
            K.judul AS judul,
            K.tanggal_rilis AS tanggal_rilis,
            K.tahun AS tahun,
            COALESCE(SUM(E.durasi), 0) AS total_durasi,
            A.nama AS podcaster
        FROM 
            konten AS K
        JOIN podcast AS P ON K.id = P.id_konten
        JOIN podcaster AS Pr ON P.email_podcaster = Pr.email
        JOIN akun AS A ON Pr.email = A.email
        LEFT JOIN episode AS E ON E.id_konten_podcast = P.id_konten
        WHERE 
            K.id = %s
        GROUP BY K.judul, K.tanggal_rilis, K.tahun, A.nama;
    """, [podcast_id])

    episodes = query_result(f"""
        SELECT 
            E.judul AS judul_episode,
            E.deskripsi AS deskripsi,
            E.durasi AS durasi,
            E.tanggal_rilis AS tanggal_rilis
        FROM 
            episode AS E
        WHERE 
            E.id_konten_podcast = %s
        ORDER BY 
            E.tanggal_rilis;
    """, [podcast_id])

    genres = query_result(f"""
        SELECT 
            G.genre AS genre
        FROM 
            genre AS G
        WHERE 
            G.id_konten = %s;
    """, [podcast_id])

    total_hours = podcast[0]['total_durasi'] // 60
    total_minutes = podcast[0]['total_durasi'] % 60

    podcast_details = {
        'judul': podcast[0]['judul'],
        'tanggal_rilis': podcast[0]['tanggal_rilis'].strftime('%d/%m/%Y'),
        'tahun': podcast[0]['tahun'],
        'total_durasi': f"{total_hours} jam {total_minutes} menit" if total_hours > 0 else f"{total_minutes} menit",
        'podcaster': podcast[0]['podcaster'],
        'genres': [genre['genre'] for genre in genres] if genres else []
    }

    episode_data = []
    for episode in episodes:
        durasi_hours = episode['durasi'] // 60
        durasi_minutes = episode['durasi'] % 60
        episode_data.append({
            'judul_episode': episode['judul_episode'],
            'deskripsi': episode['deskripsi'],
            'durasi': f"{durasi_hours} jam {durasi_minutes} menit" if durasi_hours > 0 else f"{durasi_minutes} menit",
            'tanggal_rilis': episode['tanggal_rilis']
        })

    context = {
        'podcast': podcast_details,
        'episodes': episode_data if episode_data else None,
        'message': 'Episodes not available.' if not episode_data else ''
    }

    return render(request, "podcast.html", context)


def manage_podcasts(request):
    
    if request.method == 'POST':
        roles = request.COOKIES['role']
        list_role = roles.split(" ")
        
        if "Podcaster" not in list_role:
            return HttpResponseForbidden("You are not authorized to create podcasts.")
        
        title = request.POST.get('judul')
        genres = request.POST.getlist('genre')
        email_podcaster = request.COOKIES['email']

        try:
            with connection.cursor() as cursor:
                id_konten = str(uuid.uuid4())
                cursor.execute("INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, CURRENT_TIMESTAMP, EXTRACT(YEAR FROM CURRENT_TIMESTAMP), 0)", [id_konten, title])
                cursor.execute("INSERT INTO PODCAST (id_konten, email_podcaster) VALUES (%s, %s)", [id_konten, email_podcaster])
                for genre in genres:
                    cursor.execute("INSERT INTO GENRE (id_konten, genre) VALUES (%s, %s)", [id_konten, genre])
                connection.commit()
        except Exception as e:
            connection.rollback()
            print("An error occurred: ", e)

        return HttpResponseRedirect(reverse('podcast:manage_podcasts'))

    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT K.id, K.judul AS judul,
                    COALESCE(COUNT(E.id_episode), 0) AS jumlah_episode,
                    COALESCE(SUM(E.durasi), 0) AS total_durasi
                FROM PODCAST P
                LEFT JOIN EPISODE E ON P.id_konten = E.id_konten_podcast
                LEFT JOIN KONTEN K ON P.id_konten = K.id
                GROUP BY K.id, K.judul;
            """)
            podcasts = cursor.fetchall()

        podcast_data = []
        for podcast in podcasts:
            # Unpack fetched data
            id_konten, judul, jumlah_episode, total_durasi = podcast
            total_hours = total_durasi // 60
            total_minutes = total_durasi % 60
            
            podcast_data.append({
                'id': id_konten,
                'judul': judul,
                'jumlah_episode': jumlah_episode,
                'total_durasi': f"{total_hours} jam {total_minutes} menit" if total_hours > 0 else f"{total_minutes} menit",
            })

        context = {
            'podcasts': podcast_data
        }

        return render(request, 'createPodcast.html', context)

def manage_episodes(request, podcast_id):
    if request.method == 'POST':
        roles = request.COOKIES['role']
        list_role = roles.split(" ")
        
        if "Podcaster" not in list_role:
            return HttpResponseForbidden("You are not authorized to create podcasts.")

        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        durasi = int(request.POST.get('durasi'))
        id_episode = str(uuid.uuid4())

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    [id_episode, podcast_id, judul, deskripsi, durasi]
                )

                cursor.execute(
                    """
                    UPDATE KONTEN
                    SET durasi = COALESCE(durasi, 0) + %s
                    WHERE id = %s
                    """,
                    [durasi, podcast_id]
                )

                connection.commit()

        except Exception as e:
            connection.rollback()
            print("An error occurred: ", e)

        return HttpResponseRedirect(reverse('podcast:manage_episodes', args=[podcast_id]))

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT K.judul
                FROM KONTEN K
                JOIN PODCAST P ON K.id = P.id_konten
                WHERE P.id_konten = %s
                """,
                [podcast_id]
            )
            judul_podcast = cursor.fetchone()

            cursor.execute("""
                SELECT E.id_episode,
                        E.judul AS judul_episode,
                        E.deskripsi AS deskripsi,
                        E.durasi AS durasi,
                        E.tanggal_rilis AS tanggal_rilis
                FROM EPISODE E
                WHERE E.id_konten_podcast = %s
                ORDER BY E.tanggal_rilis DESC;
            """, [podcast_id])
            episodes = cursor.fetchall()

        episode_data = []
        for episode in episodes:
            id_episode, judul_episode, deskripsi, durasi, tanggal_rilis = episode
            durasi_hours = durasi // 60
            durasi_minutes = durasi % 60

            episode_data.append({
                'id_episode': id_episode,
                'judul_episode': judul_episode,
                'deskripsi': deskripsi,
                'durasi': f"{durasi_hours} jam {durasi_minutes} menit" if durasi_hours > 0 else f"{durasi_minutes} menit",
                'tanggal_rilis': tanggal_rilis
            })

        context = {
            'podcast_id': podcast_id,
            'judul_podcast': judul_podcast,
            'episodes': episode_data
        }

        for episode in episode_data:
            print(episode)


        return render(request, 'createEpisode.html', context)



def delete_podcast(request, podcast_id):
    roles = request.COOKIES['role']
    email = request.COOKIES['email']
    print(email)

    list_role = roles.split(" ")
    print(list_role)
    
    queries = []
    
    if "Podcaster" in list_role:
        try:
            with connection.cursor() as cursor:
                # Delete episodes related to this podcast first
                cursor.execute("DELETE FROM EPISODE WHERE id_konten_podcast = %s", [podcast_id])
                # Now delete the podcast
                cursor.execute("DELETE FROM PODCAST WHERE id_konten = %s AND email_podcaster = %s", [podcast_id, email])
                cursor.execute("DELETE FROM KONTEN WHERE id = %s", [podcast_id])
                connection.commit()
        except Exception as e:
            connection.rollback()
            print("An error occurred: ", e)
        return HttpResponseRedirect(reverse('podcast:manage_podcasts'))
    else:
        return HttpResponseForbidden("You are not authorized to delete this podcast.")

def delete_episode(request, podcast_id, episode_id):
    roles = request.COOKIES['role']
    email = request.COOKIES['email']
    print(email)

    list_role = roles.split(" ")
    print(list_role)
        
    if "Podcaster" in list_role:
        try:
            with connection.cursor() as cursor:
                # Delete the episode
                cursor.execute("DELETE FROM EPISODE WHERE id_episode = %s", [episode_id])
                connection.commit()
        except Exception as e:
            connection.rollback()
            print("An error occurred: ", e)
        return HttpResponseRedirect(reverse('podcast:manage_episodes', args=[podcast_id]))
    else:
        return HttpResponseForbidden("You are not authorized to delete this episode.")

def show_chart_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_playlist, tipe
            FROM CHART;
        """)
        charts = cursor.fetchall()

    chart_data = [
        {
            'id': chart[0],
            'name': chart[1]
        } for chart in charts
    ]

    context = {
        'charts': chart_data
    }

    return render(request, 'chartList.html', context)

def show_chart_detail(request, playlist_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tipe, id_playlist
            FROM CHART
            WHERE id_playlist = %s;
        """, [playlist_id])
        chart = cursor.fetchone()
        
        if chart:
            cursor.execute("""
                SELECT K.judul, A.nama, K.tanggal_rilis, S.total_play
                FROM SONG S
                JOIN KONTEN K ON S.id_konten = K.id
                JOIN ARTIST AR ON S.id_artist = AR.id
                JOIN AKUN A ON AR.email_akun = A.email
                JOIN PLAYLIST_SONG PS ON PS.id_song = S.id_konten
                WHERE PS.id_playlist = %s;
            """, [playlist_id])
            songs = cursor.fetchall()
        else:
            songs = []

    context = {
        'chart_type': chart[0] if chart else 'No Chart Found',
        'songs': [
            {
                'title': song[0],
                'artist': song[1],
                'release_date': song[2].strftime('%d/%m/%Y'),
                'total_plays': song[3]
            } for song in songs
        ]
    }
    return render(request, 'chartDetail.html', context)
