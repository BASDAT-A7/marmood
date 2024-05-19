from django import forms

class AddPlaylistForm(forms.Form):
    judul_playlist = forms.CharField(label='Judul Playlist', max_length=100)
    deskripsi_playlist = forms.CharField(label='Deskripsi Playlist', widget=forms.Textarea)

class AddSongForm(forms.Form):
    song_artist = forms.CharField(label='Song - Artist', max_length=200)
    
class AddToPlaylistForm(forms.Form):
    playlist = forms.ChoiceField(choices=[], label='Select Playlist')

class EditPlaylistForm(forms.Form):
    judul_playlist = forms.CharField(label='Judul Playlist', max_length=100)
    deskripsi_playlist = forms.CharField(label='Deskripsi Playlist', widget=forms.Textarea)