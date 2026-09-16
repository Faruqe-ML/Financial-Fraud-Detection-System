from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models.functions import TruncDate

from dashboard.models import Transaction, CustomerProfile, Alert


def updateTrendChart():
    data = (
        Transaction.objects
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(
            total=Count('transaction_id'),
            fraud=Count(
                'transaction_id',
                filter=Q(is_fraud=True)
            ),
            safe=Count(
                'transaction_id',
                filter=Q(is_fraud=False)
            )
        )
        .order_by('date')
    )

    dates = []
    total = []
    fraud = []
    safe = []

    for row in data:
        dates.append(row['date'].strftime('%Y-%m-%d'))
        total.append(row['total'])
        fraud.append(row['fraud'])
        safe.append(row['safe'])

    return {
        'dates': dates,
        'total': total,
        'fraud': fraud,
        'safe': safe
    }

def updateTypeChart():

    data = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            total=Count("transaction_id"),
            fraud=Count(
                "transaction_id",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("transaction_type")
    )

    result = []

    for row in data:

        result.append({
            "transaction_type": row["transaction_type"],
            "total": row["total"],
            "fraud": row["fraud"],
        })

    print("TYPE CHART DATA:", result)

    return result

def updateLocationChart():

    data = (
        Transaction.objects
        .exclude(location__isnull=True)
        .exclude(location__exact="")
        .values("location")
        .annotate(
            total=Count("transaction_id"),
            fraud=Count(
                "transaction_id",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("location")
    )

    result = []

    for row in data:
        result.append({
            "location": row["location"],
            "total": row["total"],
            "fraud": row["fraud"]
        })

    print("LOCATION CHART DATA:", result)

    return result

def updateRiskChart():

    data = (
        Alert.objects
        .values("severity")
        .annotate(
            count=Count("alert_id")
        )
        .order_by("severity")
    )

    result = []

    # Keep the desired order
    severity_order = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    data_dict = {
        row["severity"]: row["count"]
        for row in data
    }

    for severity in severity_order:
        result.append({
            "label": severity,
            "count": data_dict.get(severity, 0)
        })

    print("RISK CHART DATA:", result)

    return result


def updateAlertChart():

    data = (
        Alert.objects
        .exclude(severity__isnull=True)
        .exclude(severity__exact="")
        .values("severity")
        .annotate(
            count=Count("alert_id")
        )
        .order_by("severity")
    )

    result = []

    severity_order = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    data_dict = {
        row["severity"]: row["count"]
        for row in data
    }

    for severity in severity_order:

        result.append({
            "severity": severity,
            "count": data_dict.get(severity, 0)
        })

    print("ALERT CHART DATA:", result)

    return result


def metrics():
    total_transaction = Transaction.objects.count()
    total_fraud = Transaction.objects.filter(
        is_fraud=True
    ).count()
    total_safe = Transaction.objects.filter(
        is_fraud=False
    ).count()

    if total_transaction > 0:
        fraud_rate = (total_fraud / total_transaction) * 100
    else:
        fraud_rate = 0

    total_customer = CustomerProfile.objects.count()

    active_alert = Alert.objects.filter(
        is_resolved=False
    ).count()

    return {
        "total_transaction": total_transaction,
        "total_fraud": total_fraud,
        "total_safe": total_safe,
        "fraud_rate": round(fraud_rate, 2),
        "total_customer": total_customer,
        "active_alert": active_alert,
    }

