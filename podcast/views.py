from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def show_podcast_page(request):
    return render(request, "podcast.html")

def show_chart_list(request):
    return render(request, "chartList.html")

def show_chart_detail(request):
    return render(request, "chartDetail.html")

def show_create_podcast(request):
    return render(request, "createPodcast.html")

def show_create_episode(request):
    return render(request, "createEpisode.html")