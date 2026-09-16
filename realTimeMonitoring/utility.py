from dashboard.models import Transaction


def get_live_stream_data(limit=20):

    transactions = (
        Transaction.objects
        .order_by("-timestamp")[:limit]
    )

    data = []

    for transaction in reversed(transactions):

        # ==========================================
        # STATUS
        # ==========================================

        if transaction.is_fraud:
            status = "fraud"

        elif getattr(transaction, "is_suspicious", False):
            status = "suspicious"

        elif getattr(transaction, "is_pending", False):
            status = "pending"

        else:
            status = "safe"


        # ==========================================
        # CUSTOMER
        # ==========================================

        customer = getattr(
            transaction,
            "customer_id",
            None
        )

        if customer is None:
            customer = getattr(
                transaction,
                "customer",
                None
            )

        if customer is None:
            customer = "Unknown"


        # ==========================================
        # TRANSACTION TYPE
        # ==========================================

        transaction_type = getattr(
            transaction,
            "type",
            None
        )

        if transaction_type is None:
            transaction_type = getattr(
                transaction,
                "transaction_type",
                None
            )

        if transaction_type is None:
            transaction_type = "Unknown"


        # ==========================================
        # LOCATION
        # ==========================================

        location = getattr(
            transaction,
            "location",
            None
        )

        if location is None:
            location = "Unknown"


        # ==========================================
        # ADD TRANSACTION
        # ==========================================

        data.append({

            "id": str(
                transaction.id
            ),

            "customer": str(
                customer
            ),

            "amount": float(
                transaction.amount
            ),

            "type": str(
                transaction_type
            ),

            "location": str(
                location
            ),

            "status": status,

            "time": transaction.timestamp.strftime(
                "%H:%M:%S"
            )
        })

    return data

def get_detection_rate_data(limit=50):

    transactions = (
        Transaction.objects
        .order_by("-timestamp")[:limit]
    )

    data = []

    for transaction in reversed(transactions):

        if transaction.is_fraud:
            status = "fraud"

        elif getattr(transaction, "is_suspicious", False):
            status = "suspicious"

        elif getattr(transaction, "is_pending", False):
            status = "pending"

        else:
            status = "safe"

        data.append({
            "id": str(transaction.id),
            "time": transaction.timestamp.strftime("%H:%M:%S"),
            "amount": float(transaction.amount),
            "status": status,
        })

    return data


def get_velocity_data(limit=20):

    transactions = (
        Transaction.objects
        .order_by("-timestamp")[:limit]
    )

    data = []

    for transaction in reversed(transactions):

        data.append({
            "id": str(transaction.id),
            "time": transaction.timestamp.strftime("%H:%M:%S"),
        })

    return data

def get_transaction_stats():

    total = Transaction.objects.count()

    fraud = Transaction.objects.filter(
        is_fraud=True
    ).count()

    safe = total - fraud

    pending = Transaction.objects.filter(
        is_fraud=False,
        # use your actual pending field here
    ).count()

    fraud_rate = (
        (fraud / total) * 100
        if total > 0
        else 0
    )

    return {
        "total": total,
        "safe": safe,
        "fraud": fraud,
        "pending": pending,
        "fraud_rate": round(fraud_rate, 1),
        "transactions_per_second": 0,
    }