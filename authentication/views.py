from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import ast
import datetime


def login_page(request):
    request.COOKIES['logged_in'] = "No"
    return render(request, "login.html")

def show_register(request):
    return render(request, "register.html")

def show_register_pengguna(request):
    return render(request, "registerPengguna.html")

def show_register_label(request):
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
            cursor.execute("SELECT * FROM akun WHERE email = %s AND password = %s", [email, password])
            user = cursor.fetchone()
            if user is None:
                cursor.execute("SELECT email, nama FROM label WHERE email = %s AND password = %s", [email, password])
                user = cursor.fetchone()
                
            print("ini user: ", user[0])
        
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
            print("ini response: ", response)
            print("ini role: ", role)
            print("ini role pengguna: ", role_pengguna)
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