from django.urls import path

from paket.views import show_paket

app_name = 'paket'

urlpatterns = [
    path('', show_paket, name='show_paket'),
]