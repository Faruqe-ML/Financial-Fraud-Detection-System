from django.db.models import Q
from django.db.models.aggregates import Count, Sum

from dashboard.models import Transaction, CustomerProfile, Alert


def get_risk_distribution_data():

    transactions = Transaction.objects.all()

    low_risk = 0
    medium_risk = 0
    high_risk = 0

    for transaction in transactions:

        amount = float(transaction.amount or 0)
        is_fraud = bool(transaction.is_fraud)

        # High Risk
        if is_fraud or amount >= 50000:
            high_risk += 1

        # Medium Risk
        elif amount >= 10000:
            medium_risk += 1

        # Low Risk
        else:
            low_risk += 1

    return {
        "labels": [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ],

        "values": [
            low_risk,
            medium_risk,
            high_risk
        ],

        "colors": [
            "#00D4AA",
            "#FFB432",
            "#FF6B6B"
        ]
    }


def get_segment_risk_data():

    # -----------------------------------------
    # Load required data only
    # -----------------------------------------

    transactions = Transaction.objects.values(
        "transaction_id",
        "customer_id"
    )

    customers = CustomerProfile.objects.values(
        "customer_id",
        "segment"
    )

    alerts = Alert.objects.values(
        "transaction_id",
        "severity"
    )


    # -----------------------------------------
    # Create lookup dictionaries
    # -----------------------------------------

    customer_segment = {
        row["customer_id"]: row["segment"]
        for row in customers
    }

    transaction_risk = {
        row["transaction_id"]: row["severity"]
        for row in alerts
    }


    # -----------------------------------------
    # Calculate risk by segment
    # -----------------------------------------

    result = {}


    for transaction in transactions:

        transaction_id = transaction["transaction_id"]
        customer_id = transaction["customer_id"]

        segment = customer_segment.get(
            customer_id,
            "Unknown"
        )

        severity = transaction_risk.get(
            transaction_id
        )

        # No alert = no risk category
        if not severity:
            continue

        severity = severity.strip().lower()


        # Create segment
        if segment not in result:

            result[segment] = {
                "low": 0,
                "medium": 0,
                "high": 0,
                "critical": 0
            }


        # Count transaction
        if severity == "low":

            result[segment]["low"] += 1

        elif severity == "medium":

            result[segment]["medium"] += 1

        elif severity == "high":

            result[segment]["high"] += 1

        elif severity == "critical":

            result[segment]["critical"] += 1


    # -----------------------------------------
    # Convert dictionary → list
    # -----------------------------------------

    data = []

    for segment, risk in result.items():

        data.append({
            "segment": segment,
            "low": risk["low"],
            "medium": risk["medium"],
            "high": risk["high"],
            "critical": risk["critical"]
        })


    # -----------------------------------------
    # Debug
    # -----------------------------------------

    print("\n==============================")
    print("SEGMENT RISK DATA")
    print("==============================")
    print(data)
    print("==============================\n")


    return data

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


    data = [
        {
            "label": label,
            "count": count
        }
        for label, count in ranges.items()
    ]


    print("\n==============================")
    print("RISK HISTOGRAM")
    print("==============================")

    for row in data:
        print(row)

    print("==============================\n")


    return data

def get_top_fraud_customers(limit=10):

    data = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("customer_id")
        .annotate(
            fraud_count=Count("transaction_id"),
            total_amount=Sum("amount")
        )
        .order_by("-fraud_count")[:limit]
    )

    result = []

    for row in data:

        result.append({
            "customer_name": row["customer_id"],
            "fraud_count": row["fraud_count"],
            "total_amount": float(
                row["total_amount"] or 0
            )
        })

    print("\n==============================")
    print("TOP FRAUD CUSTOMERS")
    print("==============================")

    for row in result:
        print(row)

    print("==============================\n")

    return result

def get_segment_distribution_data():

    data = (
        CustomerProfile.objects
        .values("segment")
        .annotate(count=Count("customer_id"))
        .order_by("-count")
    )

    labels = []
    values = []

    for row in data:
        labels.append(row["segment"])
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

    print("\n==============================")
    print("SEGMENT DISTRIBUTION")
    print("==============================")
    print(result)
    print("==============================\n")

    return result

def get_customer_table_data():

    low_risk = 0
    medium_risk = 0
    high_risk = 0
    critical_risk = 0

    customers = CustomerProfile.objects.values(
        "customer_id",
        "segment",
        "risk_score",
        "account_age_days",
        "location"              # ADD THIS
    )

    fraud_transactions = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("customer_id")
    )

    fraud_count_map = {}

    for transaction in fraud_transactions:

        customer_id = transaction["customer_id"]

        if customer_id not in fraud_count_map:
            fraud_count_map[customer_id] = 0

        fraud_count_map[customer_id] += 1

    result = []

    for customer in customers:

        customer_id = customer["customer_id"]

        risk_score = float(
            customer["risk_score"] or 0
        )

        risk_percentage = round(
            risk_score * 100,
            2
        )

        if risk_score < 0.25:

            risk_level = "Low"
            low_risk += 1

        elif risk_score < 0.50:

            risk_level = "Medium"
            medium_risk += 1

        elif risk_score < 0.75:

            risk_level = "High"
            high_risk += 1

        else:

            risk_level = "Critical"
            critical_risk += 1

        fraud_count = fraud_count_map.get(
            customer_id,
            0
        )

        result.append({

            "customer_id": customer_id,

            "full_name": customer_id,

            "email": "-",

            "segment":
                customer["segment"] or "",

            "risk_score":
                risk_percentage,

            "risk_level":
                risk_level,

            "account_age":
                customer["account_age_days"] or 0,

            "fraud_count":
                fraud_count,

            "location":
                customer["location"] or "",

            "low_risk":
                low_risk,

            "medium_risk":
                medium_risk,

            "high_risk":
                high_risk,

            "critical_risk":
                critical_risk,
        })

    return result


from dashboard.models import CustomerProfile, Transaction



