from django.urls import path

from . import views

app_name = "geographicAnalysis"

urlpatterns = [
    path('geographicAnalysis/<str:full_name>/', views.geographicAnalysis, name='geographicAnalysis')


]