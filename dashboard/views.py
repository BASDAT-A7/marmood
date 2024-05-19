from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functions.general import query_result
from django.db import connection

def show_dashboard(request):
    user_email = request.COOKIES.get('email')
    roles = request.COOKIES['role']
    roles_list = roles.split(" ")
    
    context = {}
    
    songs = []
    podcasts = []
    albums = []
    
    if 'Label' in roles_list:
        user_info = query_result(f"""
                            SELECT l.*
                            FROM LABEL AS l
                            WHERE l.email = '{user_email}';
                                 """)
        
        albums = query_result(f"""
                            SELECT a.*
                            FROM ALBUM AS a, LABEL AS l
                            WHERE l.id = a.id_label AND l.email = '{user_email}';
                              """)
        
        albums.extend(albums)
        
        context.update({
            'user_info': user_info,
            'albums': albums,
        })
    
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM PREMIUM WHERE email = %s", [user_email])
            is_premium = cursor.fetchone()[0] > 0
            
        if is_premium:
            status_langganan = "Premium"
        else:
            status_langganan = "Nonpremium"
            
        user_info = query_result(f"""
                            SELECT a.email
                            FROM AKUN AS a
                            WHERE a.email = '{user_email}';
                                 """)
        
        playlists = query_result(f"""
                            SELECT up.*
                            FROM USER_PLAYLIST AS up
                            WHERE up.email_pembuat = '{user_email}';
                                 """)
        
        if 'Artist' in roles_list:
            artist_songs = query_result(f"""
                                    SELECT k.judul, s.*
                                    FROM ARTIST AS a
                                    JOIN SONG AS s ON a.id = s.id_artist
                                    JOIN KONTEN AS k ON k.id = s.id_konten
                                    WHERE a.email_akun = '{user_email}';
                                        """)
            
            songs.extend(artist_songs)
            
        if 'Songwriter' in roles_list:
            songwriter_songs = query_result(f"""
                                    SELECT k.judul, s.*
                                    FROM SONGWRITER_WRITE_SONG AS sws
                                    JOIN SONGWRITER AS sw ON sws.id_songwriter = sw.id
                                    JOIN SONG AS s ON sws.id_song = s.id_konten
                                    JOIN KONTEN AS k ON k.id = s.id_konten
                                    WHERE sw.email_akun = '{user_email}';
                                            """)
            
            for song in songwriter_songs:
                if song not in songs:
                    songs.append(song)
                    
        if 'Podcaster' in roles_list:
            podcasts = query_result(f"""
                                SELECT k.judul, p.*
                                FROM PODCASTER AS pc
                                JOIN PODCAST AS p ON pc.email = p.email_podcaster
                                JOIN KONTEN AS k ON k.id = p.id_konten
                                WHERE pc.email = '{user_email}';
                                    """)
            
            podcasts.extend(podcasts)
            
        context.update({
            'user_info': user_info,
            'playlists': playlists,
            'songs': songs,
            'podcasts': podcasts,
            'status_langganan': status_langganan,
            'empty_playlists': len(playlists) == 0,
            'empty_songs': len(songs) == 0,
            'empty_podcasts': len(podcasts) == 0,
            'empty_albums': len(albums) == 0,
            'roles_list': roles_list,
        })
        
    return render(request, 'dashboard.html', context)