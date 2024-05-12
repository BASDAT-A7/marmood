from django.urls import path
from kelola_album_song.views import kelola, create_album, create_lagu

app_name = 'kelola_album_song'

urlpatterns = [
    path('', kelola, name='kelola_album_song'),
    path('create-album/', create_album, name='create-album'),
    path('create-lagu/', create_lagu, name='create-lagu')
]