from django.urls import path
from kelola_album_song.views import kelola, create_album, create_lagu, delete_lagu, delete_album, tambah_lagu, tambah_album

app_name = 'kelola_album_song'

urlpatterns = [
    path('', kelola, name='kelola_album_song'),
    path('create-album/', create_album, name='create-album'),
    path('create-lagu/', create_lagu, name='create-lagu'),
    path('delete-lagu/', delete_lagu, name='delete-lagu'),
    path('delete-album/', delete_album, name='delete-album'),
    path('create-lagu/tambah/', tambah_lagu, name='tambah-lagu'),
    path('create-album/tambah/', tambah_album, name='tambah-album')

]