from django.urls import path
from .views import (
    fetch_data,
    submit_data
)

urlpatterns = [
    path('fetch/', fetch_data, name='fetch_data'),
    path('submit/', submit_data, name='submit_data'),]