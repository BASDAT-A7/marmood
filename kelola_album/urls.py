from django.urls import path
from kelola_album.views import kelola_album, delete_album, delete_lagu

app_name = 'kelola_album'

urlpatterns = [
    path('', kelola_album, name='kelola_album'),
    path('delete-album/', delete_album, name='delete_album'),
    path('delete-lagu/', delete_lagu, name='delete_lagu'),
]