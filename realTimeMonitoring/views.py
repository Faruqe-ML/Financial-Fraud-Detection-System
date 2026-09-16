from django.shortcuts import render

from dashboard.utility import get_fraud_metrics
from realTimeMonitoring.utility import get_live_stream_data, get_detection_rate_data, get_transaction_stats


def realTimeMonitoring(request,full_name):
    live_transactions = get_live_stream_data(limit=20)
    detection_transactions = get_detection_rate_data(limit=20)
    transaction = get_transaction_stats()


    return render(request, "realTimeMonitoring/realTimeMonitoring.html", {
        "full_name":full_name,
        "live_transactions": live_transactions,
        "detection_transactions": detection_transactions,
        "transaction": transaction
    })
