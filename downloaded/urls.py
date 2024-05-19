from django.urls import path

from downloaded.views import delete_song, download_song, show_downloaded

app_name = 'downloaded'

urlpatterns = [
    path('', show_downloaded, name='show_downloaded'),
    path('delete-song/<str:id_song>', delete_song, name='delete_song'),
    path('download-song/<str:id_song>', download_song, name='download_song'),

]       