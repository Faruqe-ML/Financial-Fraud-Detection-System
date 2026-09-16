from django.shortcuts import render

from dashboard.utility import get_fraud_metrics
from geographicAnalysis.utility import get_world_map_data, get_top_countries_data, get_region_data, \
    get_location_heatmap_data, get_country_comparison_data, geographicData


# Create your views here.
# Create your views here.
def geographicAnalysis(request,full_name):
    world_map_data = get_world_map_data()
    top_countries_data = get_top_countries_data()
    region_data = get_region_data()
    location_heatmap_data = get_location_heatmap_data()
    country_comparison_data = get_country_comparison_data()
    gregraphicData = geographicData()

    return render(request, "geographicAnalysis/geographicAnalysis.html", {
        "full_name":full_name,
        "world_map_data": world_map_data,
        "top_countries_data": top_countries_data,
        "region_data": region_data,
        "location_heatmap_data": location_heatmap_data,
        "country_comparison_data": country_comparison_data,
        "gregraphicData" : gregraphicData,

    })


