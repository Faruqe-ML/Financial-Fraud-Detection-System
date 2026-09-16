from dashboard.models import Transaction, FraudCase, Alert
from django.db.models import Sum


def get_fraud_metrics():

    # =========================
    # TOTAL TRANSACTIONS
    # =========================

    total_transaction = Transaction.objects.count()

    # =========================
    # FRAUD DETECTION
    # =========================

    fraud_detection = FraudCase.objects.count()


    # =========================
    # DETECTION RATE
    # =========================

    if total_transaction > 0:

        detection_rate = (
            fraud_detection / total_transaction
        ) * 100

    else:

        detection_rate = 0


    # =========================
    # TOTAL FRAUD AMOUNT
    # =========================

    fraud_amount = (
            FraudCase.objects.aggregate(
                total=Sum("fraud_amount")
            )["total"] or 0
    )

    # Keep fraud_amount numeric
    fraud_amount_value = float(fraud_amount)

    if fraud_amount_value >= 1_00_00_000:
        fraud_amount_display = f"₹{fraud_amount_value / 1_00_00_000:.2f} Cr"
    elif fraud_amount_value >= 1_00_000:
        fraud_amount_display = f"₹{fraud_amount_value / 1_00_000:.2f} Lakh"
    elif fraud_amount_value >= 1_000:
        fraud_amount_display = f"₹{fraud_amount_value / 1_000:.2f}K"
    else:
        fraud_amount_display = f"₹{fraud_amount_value:,.0f}"

    # =========================
    # RECENT TRANSACTIONS
    # =========================

    recent_transactions = Transaction.objects.order_by(
        "-timestamp"
    )[:10]


    # =========================
    # RECENT ALERTS
    # =========================

    recent_alerts = Alert.objects.order_by(
        "-timestamp"
    )[:5]


    # =========================
    # RETURN DATA
    # =========================

    return {

        "total_transaction": total_transaction,

        "fraud_detection": fraud_detection,

        "detection_rate": round(
            detection_rate,
            2
        ),

        "fraud_amount": fraud_amount_display,

        "recent_transactions": recent_transactions,

        "recent_alerts": recent_alerts,

    }



