from django.shortcuts import render

from customer.utility import get_risk_distribution_data, get_segment_risk_data, get_risk_histogram_data, \
    get_top_fraud_customers, get_segment_distribution_data, get_customer_table_data




def customerRisk(request, full_name):

    # ==================================================
    # GRAPH DATA
    # DO NOT CHANGE
    # ==================================================

    risk_distribution_data = get_risk_distribution_data()
    segment_risk_data = get_segment_risk_data()
    risk_histogram_data = get_risk_histogram_data()
    top_fraud_customers = get_top_fraud_customers()
    segment_distribution_data = get_segment_distribution_data()

    # ==================================================
    # CUSTOMER DATA
    # ==================================================

    customer_data = get_customer_table_data()

    # ==================================================
    # TOTAL CUSTOMER
    # ==================================================

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

    # ==================================================
    # DEBUG
    # ==================================================

    print("====================================")
    print("TOTAL CUSTOMERS:", total_customer)
    print("LOW RISK:", low_risk)
    print("MEDIUM RISK:", medium_risk)
    print("HIGH RISK:", high_risk)
    print("CRITICAL RISK:", critical_risk)
    print("AVERAGE RISK SCORE:", average_risk_score)
    print("====================================")

    # ==================================================
    # RETURN
    # ==================================================

    return render(
        request,
        "customer/customerRisk.html",
        {
            "full_name": full_name,

            # ------------------------------------------
            # GRAPH DATA - UNCHANGED
            # ------------------------------------------

            "risk_distribution_data":
                risk_distribution_data,

            "segment_risk_data":
                segment_risk_data,

            "risk_histogram_data":
                risk_histogram_data,

            "top_fraud_customers":
                top_fraud_customers,

            "segment_distribution_data":
                segment_distribution_data,

            # ------------------------------------------
            # CUSTOMER TABLE
            # ------------------------------------------

            "customer_data":
                customer_data,

            # ------------------------------------------
            # CUSTOMER STATISTICS
            # ------------------------------------------

            "total_customer":
                total_customer,

            "low_risk":
                low_risk,

            "medium_risk":
                medium_risk,

            "high_risk":
                high_risk,

            "critical_risk":
                critical_risk,

            "average_risk_score":
                average_risk_score,
        }
    )




