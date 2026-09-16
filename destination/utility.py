from django.db.models.aggregates import Sum, Count

from dashboard.models import CustomerProfile, FraudCase, Transaction


def get_risk_distribution_data():

    customers = CustomerProfile.objects.values_list(
        "risk_score",
        flat=True
    )

    ranges = {
        "Low Risk": 0,
        "Medium Risk": 0,
        "High Risk": 0,
        "Critical Risk": 0,
    }

    for score in customers:

        if score is None:
            continue

        score = float(score)

        if score < 0.25:
            ranges["Low Risk"] += 1

        elif score < 0.50:
            ranges["Medium Risk"] += 1

        elif score < 0.75:
            ranges["High Risk"] += 1

        else:
            ranges["Critical Risk"] += 1

    return {
        "labels": list(ranges.keys()),
        "values": list(ranges.values()),
        "colors": [
            "#00D4AA",
            "#FFB432",
            "#FF8A8A",
            "#FF6B6B"
        ]
    }

def get_country_risk_data():

    customers = CustomerProfile.objects.values(
        "location",
        "risk_score"
    )

    country_data = {}

    for customer in customers:

        country = customer["location"] or "Unknown"
        risk_score = float(customer["risk_score"] or 0)

        if country not in country_data:
            country_data[country] = {
                "total": 0,
                "high_risk": 0
            }

        # Total customers in country
        country_data[country]["total"] += 1

        # High + Critical risk
        if risk_score >= 0.50:
            country_data[country]["high_risk"] += 1

    result = [
        {
            "country": country,
            "total": values["total"],
            "high_risk": values["high_risk"]
        }
        for country, values in country_data.items()
    ]

    # Highest number of customers first
    result.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    print("\n====================================")
    print("COUNTRY RISK DATA")
    print("TOTAL COUNTRIES:", len(result))
    print("DATA:", result[:10])
    print("====================================\n")

    return result


def get_fraud_amount_data():

    data = (
        FraudCase.objects
        .values("fraud_type")
        .annotate(
            fraud_amount=Sum("fraud_amount")
        )
        .order_by("-fraud_amount")
    )

    result = []

    for row in data:

        result.append({
            "name": row["fraud_type"] or "Unknown",
            "fraud_amount": float(
                row["fraud_amount"] or 0
            )
        })

    print("\n====================================")
    print("FRAUD AMOUNT DATA")
    print("TOTAL TYPES:", len(result))
    print("DATA:", result[:10])
    print("====================================\n")

    return result

def get_type_distribution_data():

    data = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            count=Count("transaction_id")
        )
        .order_by("-count")
    )

    labels = []
    values = []

    for row in data:

        transaction_type = (
            row["transaction_type"]
            or "Unknown"
        )

        labels.append(transaction_type)
        values.append(row["count"])

    colors = [
        "#6C3CE1",
        "#00D4AA",
        "#FFB432",
        "#FF6B6B",
        "#8B6FE8",
        "#7A7A9A"
    ]

    result = {
        "labels": labels,
        "values": values,
        "colors": [
            colors[i % len(colors)]
            for i in range(len(labels))
        ]
    }

    print("\n====================================")
    print("TYPE DISTRIBUTION DATA")
    print("DATA:", result)
    print("====================================\n")

    return result


def get_risk_histogram_data():

    customers = CustomerProfile.objects.values_list(
        "risk_score",
        flat=True
    )

    ranges = {
        "0-25%": 0,
        "25-50%": 0,
        "50-75%": 0,
        "75-100%": 0
    }

    for score in customers:

        if score is None:
            continue

        score = float(score)

        if score < 0.25:
            ranges["0-25%"] += 1

        elif score < 0.50:
            ranges["25-50%"] += 1

        elif score < 0.75:
            ranges["50-75%"] += 1

        else:
            ranges["75-100%"] += 1

    result = [
        {
            "label": label,
            "count": count
        }
        for label, count in ranges.items()
    ]

    print("\n====================================")
    print("RISK HISTOGRAM DATA")
    print("DATA:", result)
    print("====================================\n")

    return result

