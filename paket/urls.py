from django import views
from django.urls import path

from paket.views import detailed_paket, process_payment, riwayat_transaksi, show_paket

app_name = 'paket'

urlpatterns = [
    path('', show_paket, name='show_paket'),
    path('paket/<str:jenis_paket>/', detailed_paket, name='detailed_paket'),
    path('riwayattransaksi/', riwayat_transaksi, name='riwayat_transaksi'),
    path('submit-payment', process_payment, name='submit-payment'),
]