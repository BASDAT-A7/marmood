from django.urls import path
from . import views

app_name = 'playlist'

urlpatterns = [
    path('', views.page_kelola_user, name="kelola-user"),
    path('details/', views.page_user_playlist_detail, name="playlist-details"),
    path('song/', views.page_play_song, name="play-song"),
]