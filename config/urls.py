from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('', include('dashboard.urls')),
    path('', include('transaction.urls')),
    path('', include('executiveDashboard.urls')),
    path('', include('fraudAnalytics.urls')),
    path('', include('customer.urls')),
    path('', include('destination.urls')),
    path('', include('geographicAnalysis.urls')),
    path('', include('mlPerformance.urls')),
    path('', include('realTimeMonitoring.urls')),
    path('', include('alertInvestigation.urls')),
    path('chatbot/', include('chatbot.urls')),
]