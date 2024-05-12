from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#@login_required(login_url='/login')
def show_dashboard(request):
    user_profile = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'city_of_birth': 'New York',
        'gender': 'Male',
        'place_of_birth': 'New York',
        'date_of_birth': '1990-01-01',
        'role': 'Artist'
    }
    
    playlists = [
        {'name': 'Playlist 1'},
        {'name': 'Playlist 2'},
        {'name': 'Playlist 3'}
    ]

    songs = [
        {'title': 'Song 1'},
        {'title': 'Song 2'},
        {'title': 'Song 3'}
    ]

    albums = [
        {'title': 'Album 1'},
        {'title': 'Album 2'},
        {'title': 'Album 3'}
    ]

    podcasts = [
        {'title': 'Podcast 1'},
        {'title': 'Podcast 2'},
        {'title': 'Podcast 3'}
    ]

    contacts = [
        {'name': 'Contact 1', 'email': 'contact1@example.com'},
        {'name': 'Contact 2', 'email': 'contact2@example.com'}
    ]

    return render(request, 'dashboard.html', {
        'user_profile': user_profile,
        'playlists': playlists,
        'songs': songs,
        'albums': albums,
        'podcasts': podcasts,
        'contacts': contacts
    })