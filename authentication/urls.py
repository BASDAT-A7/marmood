from django.urls import path

from authentication.views import login_page, show_register, show_register_label, show_register_pengguna

app_name = 'authentication'

urlpatterns = [
    path('', login_page, name='login_page'),
    path('register', show_register, name='show_register'),
    path('register-pengguna', show_register_pengguna, name='show_register_pengguna'),
    path('register-label', show_register_label, name='show_register_label'),
]