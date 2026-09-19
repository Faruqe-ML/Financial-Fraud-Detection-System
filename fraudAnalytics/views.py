from django.shortcuts import render

from dashboard.models import FraudCase, Alert
from fraudAnalytics.utility import get_fraud_funnel_data, get_fraud_treemap_data, get_sankey_chart_data, \
    get_violin_chart_data, get_sunburst_chart_data, get_fraud_cases, get_pattern_distribution_data, \
    get_pattern_trend_data, get_severity_data, get_segment_pattern_data, get_heatmap_data


# Create your views here.


def fraudAnalytics(request, full_name):

    funnel_data = get_fraud_funnel_data()
    treemap_data = get_fraud_treemap_data()
    sankey_data = get_sankey_chart_data()
    violin_data = get_violin_chart_data()
    sunburst_data = get_sunburst_chart_data()

    # Get fraud cases data only once
    fraud_cases = get_fraud_cases()

    # Get values from dictionary
    total_fraud_cases = fraud_cases["total_fraud_cases"]
    confirmed_cases = fraud_cases["confirmed_cases"]
    under_review_cases = fraud_cases["under_review_cases"]
    false_positive_cases = fraud_cases["false_positive_cases"]
    fraud_amount = fraud_cases["fraud_amount"]

    print("Confirmed:", confirmed_cases)
    print("Under Review:", under_review_cases)
    print("False Positive:", false_positive_cases)
    print("Total Fraud Cases:", total_fraud_cases)
    print("Fraud Amount:", fraud_amount)

    return render(
        request,
        "fraudAnalytics/fraudAnalytics.html",
        {
            "full_name": full_name,

            "funnel_data": funnel_data,
            "treemap_data": treemap_data,
            "sankey_data": sankey_data,
            "violin_data": violin_data,
            "sunburst_data": sunburst_data,

            "under_review_cases": under_review_cases,
            "fraud_count": total_fraud_cases,
            "confirmed_cases": confirmed_cases,
            "false_positive_cases": false_positive_cases,
            "fraud_amount": fraud_amount,

            "fraud_cases": fraud_cases,
        }
    )




def fraudpattern(request, full_name):

    # ==================================================
    # EXISTING GRAPH DATA
    # ==================================================

    pattern_distribution_data = (
        get_pattern_distribution_data()
    )

    pattern_trend_data = (
        get_pattern_trend_data()
    )

    severity_data = get_severity_data()

    segment_pattern_data = get_segment_pattern_data()

    heatmap_data = get_heatmap_data()


    # ==================================================
    # TOTAL PATTERNS
    # ==================================================

    # Number of unique alert/fraud patterns
    total_patterns = len(
        pattern_distribution_data.get(
            "labels",
            []
        )
    )


    # ==================================================
    # DETECTED
    # ==================================================

    # Alerts that have been resolved/detected
    detected_patterns = Alert.objects.filter(
        is_resolved=True
    ).count()


    # ==================================================
    # HIGH RISK PATTERNS
    # ==================================================

    high_risk_patterns = Alert.objects.filter(
        severity__in=[
            "High",
            "Critical"
        ]
    ).count()


    # ==================================================
    # PENDING REVIEW
    # ==================================================

    # Alerts that are not resolved yet
    pending_review = Alert.objects.filter(
        is_resolved=False
    ).count()


    # ==================================================
    # DETECTION ACCURACY
    # ==================================================

    detection_accuracy = 0

    total_alerts = Alert.objects.count()

    if total_alerts > 0:

        detection_accuracy = round(
            (
                detected_patterns /
                total_alerts
            ) * 100,
            2
        )


    # ==================================================
    # TREND CHANGE
    # ==================================================

    trend_change = 0

    counts = pattern_trend_data.get(
        "counts",
        []
    )


    if len(counts) >= 2:

        previous = counts[-2]

        current = counts[-1]


        if previous != 0:

            trend_change = round(
                (
                    (
                        current -
                        previous
                    ) /
                    previous
                ) * 100,
                2
            )


    # ==================================================
    # DEBUG
    # ==================================================

    print("\n====================================")
    print(
        "TOTAL PATTERNS:",
        total_patterns
    )
    print(
        "DETECTED:",
        detected_patterns
    )
    print(
        "HIGH RISK:",
        high_risk_patterns
    )
    print(
        "PENDING REVIEW:",
        pending_review
    )
    print(
        "DETECTION ACCURACY:",
        detection_accuracy
    )
    print(
        "TREND CHANGE:",
        trend_change
    )
    print("====================================\n")


    # ==================================================
    # RETURN
    # ==================================================

    return render(
        request,
        "fraudAnalytics/fraudPattern.html",
        {
            "full_name":
                full_name,

            # ------------------------------------------
            # EXISTING GRAPH DATA
            # DO NOT CHANGE
            # ------------------------------------------

            "pattern_distribution_data":
                pattern_distribution_data,

            "pattern_trend_data":
                pattern_trend_data,

            "severity_data":
                severity_data,

            "segment_pattern_data":
                segment_pattern_data,

            "heatmap_data":
                heatmap_data,


            # ------------------------------------------
            # CARD DATA
            # ------------------------------------------

            "total_patterns":
                total_patterns,

            "detected_patterns":
                detected_patterns,

            "high_risk_patterns":
                high_risk_patterns,

            "pending_review":
                pending_review,

            "detection_accuracy":
                detection_accuracy,

            "trend_change":
                trend_change,
        }
    )
