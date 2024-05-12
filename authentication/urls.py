from django.urls import path

from authentication.views import login_page, login_view, show_register, show_register_label, show_register_pengguna
from authentication.views import login_page, login_view, show_register, show_register_label, show_register_pengguna, logout

app_name = 'authentication'

urlpatterns = [
    path('', login_view, name='login_view'),
    path('login/', login_view, name='login_view'),
    path('register', show_register, name='show_register'),
    path('register-pengguna', show_register_pengguna, name='show_register_pengguna'),
    path('register-label', show_register_label, name='show_register_label'),
    path('', logout, name='logout')
]