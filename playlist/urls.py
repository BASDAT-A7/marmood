from django.urls import path
from . import views

app_name = 'playlist'

urlpatterns = [
    path('', views.page_kelola_user, name="kelola-user"),
    path('details/<str:playlist_id>/', views.page_user_playlist_detail, name="playlist-details"),
    path('play_song/<str:song_id>', views.song_details, name="play-song"),
    path('add_song/<str:playlist_id>/', views.add_song, name='add-song'),
    path('delete_playlist/<str:playlist_id>/', views.delete_song_from_playlist, name='delete-playlist'),
    path('edit_playlist/<str:playlist_id>/', views.edit_playlist, name='edit-playlist'),
    path('add_playlist/', views.add_playlist, name='add-playlist'),
    path('delete_from_playlist/<str:playlist_id>/<str:song_id>', views.delete_song_from_playlist, name="delete-from-playlist"),
    path('download_song/<str:song_id>/', views.download_song, name='download-song'),
    path('shuffle_play/<str:playlist_id>/', views.shuffle_play, name='shuffle-play'),
    path('play_lagu/<str:song_id>', views.play_lagu, name="play-lagu")
]