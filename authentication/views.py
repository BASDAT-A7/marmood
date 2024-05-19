from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
from django.db import connection, transaction
from django.views.decorators.csrf import csrf_exempt
import ast
import datetime
import uuid, random


def login_page(request):
    request.COOKIES['logged_in'] = "No"
    return render(request, "login.html")

def show_register(request):
    return render(request, "register.html")

# @csrf_exempt
# def show_register_pengguna(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         nama = request.POST.get('nama')
#         gender = 1 if request.POST.get('gender') == 'Laki-laki' else 0
#         tempat_lahir = request.POST.get('tempat_lahir')
#         tanggal_lahir = request.POST.get('tanggal_lahir')
#         kota_asal = request.POST.get('kota_asal')
#         podcaster = request.POST.get('podcaster') == 'on'
#         artist = request.POST.get('artist') == 'on'
#         songwriter = request.POST.get('songwriter') == 'on'

#         is_verified = bool(podcaster or artist or songwriter)

#         try:
#             with transaction.atomic():  # Using transaction to ensure all queries are successful
#                 with connection.cursor() as cursor:
#                     # Check if the email is already registered
#                     cursor.execute("SELECT email FROM akun WHERE email = %s UNION SELECT email FROM label WHERE email = %s", [email, email])
#                     if cursor.fetchone():
#                         return render(request, 'registerPengguna.html', {'message': 'Email sudah terdaftar sebagai Akun atau Label.'})

#                     # Insert user into database
#                     cursor.execute("INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
#                                    [email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal])
#                     cursor.execute("INSERT INTO nonpremium VALUES (%s)", [email])

#                     if artist or songwriter:
#                         id_hak_cipta = str(uuid.uuid4())
#                         rate_royalti = random.randint(1, 500)
#                         cursor.execute(
#                             "INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES (%s, %s)",
#                             (id_hak_cipta, rate_royalti)
#                         )

#                     if podcaster:
#                         cursor.execute("INSERT INTO podcaster (email) VALUES (%s)", [email])
                        
#                     if artist:
#                         id_artist = str(uuid.uuid4())
#                         cursor.execute(
#                             "INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
#                             (id_artist, email, id_hak_cipta)
#                         )            
#                     if songwriter:
#                         id_songwriter = str(uuid.uuid4())
#                         cursor.execute(
#                             "INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
#                             (id_songwriter, email, id_hak_cipta)
#                         )
#                 # Commit all changes if all operations were successful
#                 connection.commit()

#         except Exception as e:
#             print(e)
#             connection.rollback()  # Roll back in case of error
#             return render(request, 'registerPengguna.html', {'message': 'An error occurred during registration. Please try again.'})

#         return render(request, "login.html")
#     else:
#         return render(request, "registerPengguna.html")

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def show_register_pengguna(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = 1 if request.POST.get('gender') == 'Laki-laki' else 0
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        podcaster = request.POST.get('podcaster') == 'on'
        artist = request.POST.get('artist') == 'on'
        songwriter = request.POST.get('songwriter') == 'on'

        is_verified = bool(podcaster or artist or songwriter)

        print(f"Data yang diterima: email={email}, password={password}, nama={nama}, gender={gender}, tempat_lahir={tempat_lahir}, tanggal_lahir={tanggal_lahir}, kota_asal={kota_asal}, podcaster={podcaster}, artist={artist}, songwriter={songwriter}")

        try:
            with transaction.atomic():  # Menggunakan transaction untuk memastikan semua query sukses
                with connection.cursor() as cursor:
                    # Check if the email is already registered
                    cursor.execute("SELECT email FROM akun WHERE email = %s UNION SELECT email FROM label WHERE email = %s", [email, email])
                    if cursor.fetchone():
                        return render(request, 'registerPengguna.html', {'message': 'Email sudah terdaftar sebagai Akun atau Label.'})

                    # Insert user into database
                    cursor.execute("INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                   [email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal])
                    cursor.execute("INSERT INTO nonpremium VALUES (%s)", [email])

                    if artist or songwriter:
                        id_hak_cipta = str(uuid.uuid4())
                        rate_royalti = random.randint(1, 500)
                        cursor.execute(
                            "INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES (%s, %s)",
                            (id_hak_cipta, rate_royalti)
                        )

                    if podcaster:
                        cursor.execute("INSERT INTO podcaster (email) VALUES (%s)", [email])

                    if artist:
                        id_artist = str(uuid.uuid4())
                        cursor.execute(
                            "INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                            (id_artist, email, id_hak_cipta)
                        )
                        print(f"Artist added with id: {id_artist}")

                    if songwriter:
                        id_songwriter = str(uuid.uuid4())
                        cursor.execute(
                            "INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                            (id_songwriter, email, id_hak_cipta)
                        )
                        print(f"Songwriter added with id: {id_songwriter}")

        except Exception as e:
            print(e)
            return render(request, 'registerPengguna.html', {'message': 'An error occurred during registration. Please try again.'})

        return render(request, "login.html")
    else:
        return render(request, "registerPengguna.html")


@csrf_exempt
def show_register_label(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')

        print(f"Data yang diterima: email={email}, password={password}, nama={nama}, kontak={kontak}")

        try:
            with transaction.atomic():  # Ensure all database operations are transactional
                with connection.cursor() as cursor:
                    # Check if the email is already registered in 'akun' or 'label'
                    cursor.execute("SELECT email FROM akun WHERE email = %s UNION SELECT email FROM label WHERE email = %s", [email, email])
                    if cursor.fetchone():
                        return render(request, 'registerLabel.html', {'message': 'Email sudah terdaftar sebagai Akun atau Label.'})

                    id_label = str(uuid.uuid4())
                    id_pemilik_hak_cipta = str(uuid.uuid4())
                    rate_royalti = random.randint(1, 500)

                    print(f"Inserting pemilik_hak_cipta with id={id_pemilik_hak_cipta}")

                    # Insert pemilik_hak_cipta into database
                    cursor.execute(
                        "INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES (%s, %s)",
                        [id_pemilik_hak_cipta, rate_royalti]
                    )

                    print(f"Inserting label with id={id_label} and pemilik_hak_cipta id={id_pemilik_hak_cipta}")

                    # Insert label into database
                    cursor.execute(
                        "INSERT INTO label (id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES (%s, %s, %s, %s, %s, %s)",
                        [id_label, nama, email, password, kontak, id_pemilik_hak_cipta]
                    )

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)
            return render(request, 'registerLabel.html', {'message': 'Error registering label: {}'.format(str(e))})

        return render(request, "login.html")
    else:
        return render(request, "registerLabel.html")




@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Mendapatkan data dari permintaan POST
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("ini email: ", email)
        print("ini password: ", password)

        # Lakukan proses autentikasi di sini
        with connection.cursor() as cursor:
            cursor.execute("SELECT email, nama FROM akun WHERE email = %s AND password = %s", [email, password])
            user = cursor.fetchone()
            if user is None:
                cursor.execute("SELECT email, nama FROM label WHERE email = %s AND password = %s", [email, password])
                user = cursor.fetchone()
                
            # print("user", user[0])
        
        if user:
            # Pengguna ditemukan, autentikasi berhasil
            # Menyeleksi role pengguna
            role_pengguna = ""

            # Untuk role Artist (UUID, email, UUID Hak Cipta)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM artist WHERE email_akun = %s", [email])
                role = cursor.fetchone()

            if role:
                role_pengguna += ("Artist ")

            # Untuk role Songwriter (UUID, email, UUID Hak Cipta)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Songwriter WHERE email_akun = %s", [email])
                role = cursor.fetchone()
            
            if role:
                role_pengguna += ("Songwriter ")

            # Untuk role Podcaster (email)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM podcaster WHERE email = %s", [email])
                role = cursor.fetchone()

            if role:
                role_pengguna += ("Podcaster ")

            # Untuk role Premium (email)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM premium WHERE email = %s", [email])
                role = cursor.fetchone()

            if role:
                role_pengguna += ("Premium ")

            # Untuk role Label (UUID, nama, email, password, kontak, UUID Hak Cipta)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM label WHERE email = %s", [email])
                role = cursor.fetchone()

            if role:
                role_pengguna += ("Label ")
            
            response = HttpResponseRedirect(reverse("cek_royalti:cek_royalti")) 
            response.set_cookie('email', user[0], max_age=3600)  # Simpan informasi autentikasi di cookie
            response.set_cookie('nama', user[1], max_age=3600)  # Simpan informasi autentikasi di cookie
            response.set_cookie('role', role_pengguna, max_age=3600)  # Simpan informasi autentikasi di cookie
            response.set_cookie('logged_in', "Yes", max_age=3600)  # Simpan informasi autentikasi di cookie
            return response
        else:
            return render(request, 'login.html')
        
    response = HttpResponse(render(request, 'login.html'))
    response.delete_cookie('email')
    response.delete_cookie('logged_in')
    response.delete_cookie('nama')
    response.delete_cookie('role')
    return response

def logout(request):
    response = HttpResponse(render(request, 'login.html'))
    response.delete_cookie('email')
    response.delete_cookie('logged_in')
    response.delete_cookie('nama')
    response.delete_cookie('role')
    return response