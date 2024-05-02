from django.urls import path
from kelola_album.views import kelola_album

app_name = 'kelola_album'

urlpatterns = [
    path('', kelola_album, name='kelola_album'),
]