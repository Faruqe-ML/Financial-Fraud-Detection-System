from django.shortcuts import render

from customer.utility import get_customer_table_data
from destination.utility import get_risk_distribution_data, get_country_risk_data, get_fraud_amount_data, \
    get_type_distribution_data, get_risk_histogram_data


def destination(request,full_name):
    risk_distribution_data = get_risk_distribution_data()
    country_risk_data = get_country_risk_data()
    fraud_amount_data = get_fraud_amount_data()
    type_distribution_data = get_type_distribution_data()
    risk_histogram_data = get_risk_histogram_data()
    customer_data = get_customer_table_data()
    total_customer = len(customer_data)

    # ==================================================
    # RISK COUNTS
    # ==================================================

    low_risk = 0
    medium_risk = 0
    high_risk = 0
    critical_risk = 0

    total_risk_score = 0

    # ==================================================
    # CALCULATE RISK STATISTICS
    # ==================================================

    for customer in customer_data:

        risk_score = float(
            customer.get("risk_score", 0) or 0
        )

        # risk_score from get_customer_table_data()
        # is already converted to percentage.
        #
        # Example:
        # 0.697657 -> 69.7657

        total_risk_score += risk_score

        # ------------------------------------------------
        # RISK LEVEL
        # ------------------------------------------------

        if risk_score < 25:

            low_risk += 1

        elif risk_score < 50:

            medium_risk += 1

        elif risk_score < 75:

            high_risk += 1

        else:

            critical_risk += 1

    # ==================================================
    # AVERAGE RISK SCORE
    # ==================================================

    if total_customer > 0:

        average_risk_score = round(
            total_risk_score / total_customer,
            2
        )

    else:

        average_risk_score = 0

    total_destination = len(set(
        customer["location"]
        for customer in customer_data
        if customer.get("location")
    ))

    return render(request, "destination/destination.html", {
        "full_name":full_name,
        "risk_distribution_data": risk_distribution_data,
        "country_risk_data": country_risk_data,
        "fraud_amount_data": fraud_amount_data,
        "type_distribution_data":type_distribution_data,
        "risk_histogram_data": risk_histogram_data,
        "total_destination" : total_destination,
        "low_risk": low_risk,
        "medium_risk" : medium_risk,
        "high_risk" : high_risk,
        "critical_risk" : critical_risk,
        "average_risk_score" : average_risk_score,


    })
