from django.urls import path

from . import views

app_name = "customer"

urlpatterns = [
    path('customerRisk/<str:full_name>/', views.customerRisk, name='customerRisk'),



]