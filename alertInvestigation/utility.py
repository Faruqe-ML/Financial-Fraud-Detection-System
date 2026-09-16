from dashboard.models import Transaction


def get_severity(amount, is_fraud):
    """
    Calculate transaction severity.
    """

    amount = float(amount or 0)

    # Fraud transaction
    if is_fraud:
        if amount >= 1000000:
            return "critical"
        elif amount >= 100000:
            return "high"
        else:
            return "medium"

    # Non-fraud transaction
    if amount >= 1000000:
        return "high"
    elif amount >= 100000:
        return "medium"
    else:
        return "low"


def get_severity_data(limit=50):

    transactions = (
        Transaction.objects
        .order_by("-id")[:limit]
    )

    data = []

    for transaction in transactions:

        severity = get_severity(
            transaction.amount,
            transaction.is_fraud
        )

        data.append({
            "id": transaction.id,
            "amount": float(transaction.amount),
            "severity": severity,
            "status": (
                "fraud"
                if transaction.is_fraud
                else "safe"
            )
        })

    return data

def get_status_data(limit=50):

    transactions = (
        Transaction.objects
        .order_by("-id")[:limit]
    )

    data = []

    for transaction in transactions:

        # Determine alert status
        if transaction.is_fraud:
            status = "confirmed"
        else:
            status = "resolved"

        data.append({
            "id": transaction.id,
            "amount": float(transaction.amount),
            "status": status
        })

    return data

def get_alert_stats():

    transactions = Transaction.objects.all()

    total = transactions.count()

    critical = transactions.filter(
        is_fraud=True
    ).count()

    # Currently treating non-fraud transactions as resolved.
    resolved = transactions.filter(
        is_fraud=False
    ).count()

    open_alerts = 0
    investigating = 0

    resolution_rate = (
        (resolved / total) * 100
        if total > 0
        else 0
    )

    print("Total:", total)
    print("Critical:", critical)
    print("Open:", open_alerts)
    print("Investigating:", investigating)
    print("Resolved:", resolved)
    print("Resolution Rate:", round(resolution_rate, 1))



    return {
        "total": total,
        "critical": critical,
        "open": open_alerts,
        "investigating": investigating,
        "resolved": resolved,
        "resolution_rate": round(resolution_rate, 1),
    }