from django.urls import path # type: ignore
from cek_royalti.views import cek

app_name = 'cek_royalti'

urlpatterns = [
    path('', cek, name='cek_royalti'),
]