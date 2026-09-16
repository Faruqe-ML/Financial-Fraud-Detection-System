from django.urls import path

from . import views

app_name = "fraudAnalytics"

urlpatterns = [
    path('fraudAnalytics/<str:full_name>/', views.fraudAnalytics, name='fraudAnalytics'),
    path('fraudpattern/<str:full_name>/', views.fraudpattern, name='fraudpattern'),


]