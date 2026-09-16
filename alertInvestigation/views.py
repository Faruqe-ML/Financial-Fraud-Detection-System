from django.shortcuts import render

from alertInvestigation.utility import get_severity_data, get_status_data, get_alert_stats
from dashboard.utility import get_fraud_metrics


def alertInvestigation(request,full_name):

    severity_data = get_severity_data(limit=50)
    status_data = get_status_data(limit=50)
    alert_stats = get_alert_stats()
    return render(request, "alertInvestigation/alertInvestigation.html", {
        "full_name":full_name,
        "severity_data": severity_data,
        "status_data": status_data,
        "alert_stats": alert_stats,
    })
