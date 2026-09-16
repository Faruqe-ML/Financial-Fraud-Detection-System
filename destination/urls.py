from django.urls import path

from . import views

app_name = "destination"

urlpatterns = [
    path('destination/<str:full_name>/', views.destination, name='destination')


]