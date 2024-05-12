"""
URL configuration for marmood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("authentication.urls")),
    path('kelola-album-song/', include('kelola_album_song.urls')),
    path('cek-royalti/', include('cek_royalti.urls')),
    path('kelola-album/', include('kelola_album.urls')),
    path('paket/', include('paket.urls')),
    path('downloaded/', include('downloaded.urls')),
    path('podcast/', include('podcast.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('playlist/', include('playlist.urls')),
]
