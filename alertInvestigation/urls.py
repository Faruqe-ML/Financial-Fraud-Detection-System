from django.urls import path

from . import views

app_name = "alertInvestigation"

urlpatterns = [
    path('alertInvestigation/<str:full_name>/', views.alertInvestigation, name='alertInvestigation')


]