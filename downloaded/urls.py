from django.urls import path

from downloaded.views import show_deleted, show_downloaded

app_name = 'downloaded'

urlpatterns = [
    path('', show_downloaded, name='show_downloaded'),
    path('deleted', show_deleted, name='show_deleted'),
]