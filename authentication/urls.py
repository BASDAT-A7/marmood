from django.urls import path

from authentication.views import login_page

app_name = 'authentication'

urlpatterns = [
    path('', login_page, name='login_page'),
]