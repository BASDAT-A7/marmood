from django.shortcuts import render

def page_kelola_user(request):
    return render(request, 'playlist_page.html')

def page_user_playlist_detail(request):
    return render(request, 'playlist_details.html')

def page_play_song(request):
    return render(request, "play_song.html")