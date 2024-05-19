from django.shortcuts import render
from django.db import connection

# Create your views here.
def cek(request):
    context = {}

    return render(request, "cek_royalti.html", context)

def tampil_data(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM artist")
    data = cursor.fetchall()
    cursor.close()


    context = {
        'data': data
    }
    return render(request, 'cek_royalti.html', context)

def data_royalti(request):
    roles = request.COOKIES['role']
    email = request.COOKIES['email']
    list_role = roles.split(" ")

    
    queries = []
    
    if "Artist" in list_role or ("Songwriter" in list_role):
        # Cari UUID dan id_pemilik_hak_cipta nya pake email di cookie
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT K.judul, AL.judul, S.total_play, S.total_download, S.total_play * P.rate_royalti " +
                       "FROM konten K, album AL, artist AR, song S, pemilik_hak_cipta P  " +
                       "WHERE AR.email_akun = %s AND AR.id_pemilik_hak_cipta = P.id AND AR.id = S.id_artist AND S.id_konten = K.id AND S.id_album = AL.id " +
                       "UNION " +
                       "(SELECT DISTINCT K.judul, AL.judul, S.total_play, S.total_download, S.total_play * P.rate_royalti " +
                       "FROM konten K, album AL, songwriter SW, song S, pemilik_hak_cipta P, songwriter_write_song SWS " + 
                       "WHERE SW.email_akun = %s AND SW.id = SWS.id_songwriter AND SWS.id_song = S.id_konten AND SW.id_pemilik_hak_cipta = P.id AND S.id_konten = K.id AND S.id_album = AL.id)", [email, email])
        data = cursor.fetchall()
        cursor.close()
        queries += data
        
    if "Label" in list_role:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT K.judul, AL.judul, S.total_play, S.total_download, S.total_play * P.rate_royalti " +
                       "FROM konten K, album AL, label L, song S, pemilik_hak_cipta P  " +
                       "WHERE L.email = %s AND L.id_pemilik_hak_cipta = P.id AND L.id = AL.id_label AND AL.id = S.id_album AND S.id_konten = K.id", [email])
        data = cursor.fetchall()
        cursor.close()
        queries += data

    context = {
        'nama' : request.COOKIES['nama'],
        'queries' : queries
    }
    return render(request, "cek_royalti.html", context)
