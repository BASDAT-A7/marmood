from django.urls import path
from podcast.views import show_podcast_page, show_chart_list, show_chart_detail, show_create_podcast, show_create_episode
from podcast.views import show_register, show_register_pengguna, show_register_label

app_name = 'podcast'

urlpatterns = [
    path('', show_podcast_page, name='show_podcast_page'),
    path('chart-list', show_chart_list, name='show_chart_list'),
    path('chart-detail', show_chart_detail, name='show_chart_detail'),
    path('create-podcast', show_create_podcast, name='show_create_podcast'),
    path('create-episode', show_create_episode, name='show_create_episode'),
    path('register', show_register, name='show_register'),
    path('register-pengguna', show_register_pengguna, name='show_register_pengguna'),
    path('register-label', show_register_label, name='show_register_label'),
]