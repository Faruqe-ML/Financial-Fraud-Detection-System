from django.urls import path

from . import views

app_name = "transaction"

urlpatterns = [
    path('transaction/<str:full_name>/', views.transaction, name='transaction'),
    path('transaction_history/<str:full_name>/', views.transaction_history, name='transaction_history'),
    path('transactionAnalytics/<str:full_name>/', views.transactionAnalytics, name='transactionAnalytics'),
    path("fraud-detection/<str:full_name>/",views.fraud_detection,name="fraud_detection"),
    path("transaction_data/<str:transaction_id>/",views.get_transaction,name="get_transaction"),

]