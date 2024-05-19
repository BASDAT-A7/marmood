from django.urls import path
from . import views

app_name = 'playlist'

urlpatterns = [
    path('', views.page_kelola_user, name="kelola-user"),
    path('details/<int:playlist_id>/', views.page_user_playlist_detail, name="playlist-details"),
    path('song/<str:song_id>', views.song_details, name="play-song"),
    path('add_song/<int:playlist_id>/', views.add_song, name='add-song'),
    path('delete_playlist/<int:playlist_id>/', views.delete_song_from_playlist, name='delete-playlist'),
    path('edit_playlist/<int:playlist_id>/', views.edit_playlist, name='edit-playlist'),
    path('add_playlist/', views.add_playlist, name='add-playlist'),
    path('delete_from_playlist/<int:playlist_id>/<int:song_id>', views.delete_song_from_playlist, name="delete-from-playlist"),
    path('download_song/<int:song_id>/', views.download_song, name='download-song'),
    path('shuffle-play/<int:playlist_id>/', views.shuffle_play, name='shuffle-play'),
    path('play-song/<int:song_id>', views.play_lagu, name="actually-play-song")
]