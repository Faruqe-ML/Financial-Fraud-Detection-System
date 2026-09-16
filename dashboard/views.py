from django.contrib.auth import logout
from django.shortcuts import render, redirect

from dashboard.utility import get_fraud_metrics

def dashboard(request):


    metrics = get_fraud_metrics()
    full_name = request.session.get("full_name")
    return render(request, "dashboard/dashboard.html", {"metrics": metrics, "full_name":full_name})


def user_logout(request):
    logout(request)
    return redirect('homepage:homepage')