from django.urls import path

from . import views

app_name = "executiveDashboard"

urlpatterns = [
    path('executiveDashboard/<str:full_name>/', views.executiveDashboard, name='executiveDashboard'),


]