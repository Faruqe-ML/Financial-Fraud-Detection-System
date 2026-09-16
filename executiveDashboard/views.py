from django.shortcuts import render

from executiveDashboard.utility import updateTrendChart, updateTypeChart, updateLocationChart, updateRiskChart, \
    updateAlertChart,  metrics


# Create your views here.


def executiveDashboard(request,full_name):

    trend_chart = updateTrendChart()
    type_chart = updateTypeChart()
    location_chart = updateLocationChart()
    risk_chart = updateRiskChart()
    alert_chart = updateAlertChart()
    metric = metrics()
    return render(request, "executiveDashboard/executiveDashboard.html",
                  {"full_name": full_name,
                   "trend_chart":trend_chart,
                   "type_chart": type_chart,
                   "location_chart": location_chart,
                   "risk_chart":risk_chart,
                   "alert_chart": alert_chart,
                   "metrics":metric})