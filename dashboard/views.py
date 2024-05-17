from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functions.general import query_result

@login_required(login_url='/login')
def show_dashboard(request):
    user_email = request.COOKIES.get('email')
    roles = request.COOKIES.get('role')
    
    if roles:
        roles_list = roles.split(',')
    
    context = {}
    
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
        
        context.update({
            'user_info': user_info,
            'albums': albums,
        })
    
    else:
        user_info = query_result(f"""
                            SELECT a.*
                            FROM AKUN AS a
                            WHERE a.email = '{user_email}';
                                 """)
        
        playlists = query_result(f"""
                            SELECT up.*
                            FROM USERPLAYLIST AS up
                            WHERE up.email_pembuat = '{user_email}';
                                 """)
        
        songs = []
        
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
                                    FROM SONGWRITERWRITESONG AS sws
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
            
        context.update({
            'user_info': user_info,
            'playlists': playlists,
            'songs': songs if 'Artist' in roles_list or 'Songwriter' in roles_list else None,
            'podcasts': podcasts if 'Podcaster' in roles_list else None,
        })
        
    return render(request, 'dashboard.html', context)