from django.urls import path

from . import views

app_name = "homepage"


urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('choose/', views.choose, name='choose'),

    path('register/', views.register, name='register'),

    path('submit_registration/',views.submit_registration, name='submit_registration'),

    path('verify_otp/',views.verify_otp,name='verify_otp'),

    path('verify_otp2/',views.verify_otp2,name='verify_otp2'),

    path('login/', views.login, name='login'),

    path('login_view/',views.login_view,name='login_view'),

]