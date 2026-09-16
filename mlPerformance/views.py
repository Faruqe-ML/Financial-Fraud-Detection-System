from django.shortcuts import render

from mlPerformance.utility import get_performance_data, get_confusion_matrix_data, get_roc_data, \
    get_feature_importance_data


def mlPerformance(request,full_name):
    performance_data = get_performance_data()
    confusion_matrix_data = (
        get_confusion_matrix_data()
    )
    roc_data = get_roc_data()

    feature_importance_data = (
        get_feature_importance_data()
    )


    return render(request, "mlPerformance/mlPerformance.html", {
        "full_name":full_name,
        "performance_data": performance_data,
        "confusion_matrix_data":
            confusion_matrix_data,
        "roc_data":
            roc_data,
        "feature_importance_data":
            feature_importance_data,
    })
