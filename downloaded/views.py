from datetime import datetime
from django.db import connection
from django.shortcuts import render

from functions.general import query_result

def show_downloaded(request):
    email = request.COOKIES["email"]
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    songs_downloaded = query_result(f"""
        SELECT 
            DS.id_song AS "id_lagu",
            K.judul AS "judul_lagu", 
            AK.nama AS "oleh"
        FROM 
            DOWNLOADED_SONG DS
        JOIN 
            SONG S ON DS.id_song = S.id_konten
        JOIN 
            KONTEN K ON S.id_konten = K.id
        JOIN 
            ARTIST A ON S.id_artist = A.id
        JOIN 
            AKUN AK ON A.email_akun = AK.email
        WHERE 
            DS.email_downloader = %s;
        """, ([email]))
    context = {
        'songs': songs_downloaded,
        'date': current_date
    }
    print(songs_downloaded)
    return render(request, "downloaded.html", context)

def delete_song(request, id_song): #delete songs 
    email = request.COOKIES["email"]
    with connection.cursor() as cursor:
        try:
            # Start transaction by deleting a record from DOWNLOADED_SONG
            cursor.execute("""
                DELETE FROM DOWNLOADED_SONG
                WHERE email_downloader = %s AND id_song = %s;
            """, (email, id_song))
            if cursor.rowcount > 0:
                cursor.execute("""
                    UPDATE SONG
                    SET total_download = total_download - 1
                    WHERE id_konten = %s AND total_download > 0;
                """, (id_song,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"An error occurred: {e}")
        


    return render(request, "deleted.html")

def download_song(request, id_song):
    email = request.COOKIES.get("email", None)
    songs_title = query_result(f"""
        SELECT judul FROM KONTEN
        WHERE id = %s
        """, (id_song,))

    result = query_result(f"""
        BEGIN;

        INSERT INTO DOWNLOADED_SONG (id_song, email_downloader)
        VALUES (%s, %s);

        UPDATE SONG
        SET total_download = total_download + 1
        WHERE id_konten = %s;

        COMMIT;
        """, (id_song, email, id_song))

    context = {
        "judul_lagu": songs_title[0]['judul']
    }
    return render(request, "download_status.html", context)
