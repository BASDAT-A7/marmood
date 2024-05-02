from django.urls import path
from podcast.views import show_podcast_page, show_chart_list, show_chart_detail, show_create_podcast, show_create_episode

app_name = 'podcast'

urlpatterns = [
    path('', show_podcast_page, name='show_podcast_page'),
    path('chart-list', show_chart_list, name='show_chart_list'),
    path('chart-detail', show_chart_detail, name='show_chart_detail'),
    path('create-podcast', show_create_podcast, name='show_create_podcast'),
    path('create-episode', show_create_episode, name='show_create_episode'),
]