from django.urls import path
from search_songs.views import search_songs

app_name = 'search_songs'
urlpatterns = [
    path('', search_songs, name='search_songs'),
]