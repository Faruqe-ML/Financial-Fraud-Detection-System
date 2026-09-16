from django.urls import path

from . import views

app_name = "mlPerformance"

urlpatterns = [
    path('mlPerformance/<str:full_name>/', views.mlPerformance, name='mlPerformance')


]