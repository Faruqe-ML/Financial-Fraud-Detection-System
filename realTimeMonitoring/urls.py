from django.urls import path

from . import views

app_name = "realTimeMonitoring"

urlpatterns = [
    path('realTimeMonitoring/<str:full_name>/', views.realTimeMonitoring, name='realTimeMonitoring')


]