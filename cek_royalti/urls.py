from django.urls import path # type: ignore
from cek_royalti.views import cek, tampil_data, data_royalti

app_name = 'cek_royalti'

urlpatterns = [
    path('', data_royalti, name='cek_royalti'),
    path('query/', tampil_data, name='query_cek_royalti'),


]