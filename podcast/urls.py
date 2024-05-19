from django.urls import path
from podcast.views import show_chart_list, show_chart_detail
from podcast.views import show_detail_podcast, manage_podcasts, manage_episodes, delete_podcast, delete_episode

app_name = 'podcast'

urlpatterns = [
    path('', manage_podcasts, name='manage_podcasts'),
    path('<str:podcast_id>/', show_detail_podcast, name='show_detail_podcast'),
    path('manage-episodes/<str:podcast_id>/', manage_episodes, name='manage_episodes'),
    path('delete-podcast/<str:podcast_id>/', delete_podcast, name='delete_podcast'),
    path('delete-episode/<str:podcast_id>/<str:episode_id>/', delete_episode, name='delete_episode'),
    path('chart-list', show_chart_list, name='show_chart_list'),
    path('chart-detail/<str:playlist_id>/', show_chart_detail, name='show_chart_detail'),
]