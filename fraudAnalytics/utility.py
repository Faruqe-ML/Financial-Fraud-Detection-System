from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import TruncDate

from dashboard.models import Transaction, FraudCase, Alert, CustomerProfile


def get_fraud_funnel_data():

    # ==========================================
    # STAGE 1
    # ALL TRANSACTIONS
    # ==========================================

    total_transactions = Transaction.objects.count()


    # ==========================================
    # STAGE 2
    # UNUSUAL TRANSACTIONS
    #
    # New device OR card not present
    # ==========================================

    unusual_transactions = Transaction.objects.filter(
        Q(is_new_device=True) |
        Q(card_present=False)
    ).count()


    # ==========================================
    # STAGE 3
    # HIGH-RISK TRANSACTIONS
    #
    # New device AND card not present
    # ==========================================

    high_risk_transactions = Transaction.objects.filter(
        is_new_device=True,
        card_present=False
    ).count()


    # ==========================================
    # STAGE 4
    # FRAUDULENT TRANSACTIONS
    #
    # Fraud + new device + card not present
    # ==========================================

    fraudulent_transactions = Transaction.objects.filter(
        is_fraud=True,
        is_new_device=True,
        card_present=False
    ).count()


    # ==========================================
    # RETURN DATA
    # ==========================================
    print("Total Transactions:", total_transactions)
    print("Unusual Transactions:", unusual_transactions)
    print("High Risk Transactions:", high_risk_transactions)
    print("Fraudulent Transactions:", fraudulent_transactions)
    return {
        "stages": [
            "All Transactions",
            "Unusual Transactions",
            "High-Risk Transactions",
            "Fraudulent Transactions"
        ],

        "values": [
            total_transactions,
            unusual_transactions,
            high_risk_transactions,
            fraudulent_transactions
        ]
    }

def get_fraud_treemap_data():

    fraud_data = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("transaction_type")
        .annotate(
            count=Count("id"),
            total_amount=Sum("amount")
        )
        .order_by("-count")
    )

    data = []

    for row in fraud_data:
        data.append({
            "fraud_type": row["transaction_type"],
            "count": row["count"],
            "total_amount": float(row["total_amount"] or 0)
        })

    return data

def get_sankey_chart_data():

    # =========================================
    # NODE DEFINITIONS
    # =========================================

    nodes = [
        "Card Present",
        "Card Not Present",
        "New Device",
        "Existing Device",
        "Safe Transactions",
        "Fraudulent Transactions"
    ]


    # =========================================
    # NODE INDEX
    # =========================================

    node_index = {
        name: index
        for index, name in enumerate(nodes)
    }


    # =========================================
    # LINKS
    # =========================================

    links = []


    # -----------------------------------------
    # CARD PRESENT → DEVICE STATUS
    # -----------------------------------------

    card_present_new_device = Transaction.objects.filter(
        card_present=True,
        is_new_device=True
    ).count()

    card_present_existing_device = Transaction.objects.filter(
        card_present=True,
        is_new_device=False
    ).count()


    # -----------------------------------------
    # CARD NOT PRESENT → DEVICE STATUS
    # -----------------------------------------

    card_not_present_new_device = Transaction.objects.filter(
        card_present=False,
        is_new_device=True
    ).count()

    card_not_present_existing_device = Transaction.objects.filter(
        card_present=False,
        is_new_device=False
    ).count()


    # =========================================
    # CARD PRESENT FLOWS
    # =========================================

    if card_present_new_device > 0:

        links.append({
            "source": node_index["Card Present"],
            "target": node_index["New Device"],
            "value": card_present_new_device
        })


    if card_present_existing_device > 0:

        links.append({
            "source": node_index["Card Present"],
            "target": node_index["Existing Device"],
            "value": card_present_existing_device
        })


    # =========================================
    # CARD NOT PRESENT FLOWS
    # =========================================

    if card_not_present_new_device > 0:

        links.append({
            "source": node_index["Card Not Present"],
            "target": node_index["New Device"],
            "value": card_not_present_new_device
        })


    if card_not_present_existing_device > 0:

        links.append({
            "source": node_index["Card Not Present"],
            "target": node_index["Existing Device"],
            "value": card_not_present_existing_device
        })


    # =========================================
    # DEVICE → FRAUD STATUS
    # =========================================

    new_device_safe = Transaction.objects.filter(
        is_new_device=True,
        is_fraud=False
    ).count()

    new_device_fraud = Transaction.objects.filter(
        is_new_device=True,
        is_fraud=True
    ).count()

    existing_device_safe = Transaction.objects.filter(
        is_new_device=False,
        is_fraud=False
    ).count()

    existing_device_fraud = Transaction.objects.filter(
        is_new_device=False,
        is_fraud=True
    ).count()


    # =========================================
    # NEW DEVICE → STATUS
    # =========================================

    if new_device_safe > 0:

        links.append({
            "source": node_index["New Device"],
            "target": node_index["Safe Transactions"],
            "value": new_device_safe
        })


    if new_device_fraud > 0:

        links.append({
            "source": node_index["New Device"],
            "target": node_index["Fraudulent Transactions"],
            "value": new_device_fraud
        })


    # =========================================
    # EXISTING DEVICE → STATUS
    # =========================================

    if existing_device_safe > 0:

        links.append({
            "source": node_index["Existing Device"],
            "target": node_index["Safe Transactions"],
            "value": existing_device_safe
        })


    if existing_device_fraud > 0:

        links.append({
            "source": node_index["Existing Device"],
            "target": node_index["Fraudulent Transactions"],
            "value": existing_device_fraud
        })


    # =========================================
    # RETURN DATA
    # =========================================

    return {
        "nodes": nodes,
        "links": links
    }


def get_violin_chart_data():

    # =========================================
    # GET FRAUD TRANSACTIONS
    # =========================================

    fraud_transactions = (
        Transaction.objects
        .filter(is_fraud=True)
        .values(
            "transaction_type",
            "amount"
        )
        .order_by("transaction_type")
    )


    # =========================================
    # GROUP AMOUNTS BY TRANSACTION TYPE
    # =========================================

    grouped_data = {}

    for row in fraud_transactions:

        transaction_type = (
            row["transaction_type"]
        )

        amount = row["amount"]


        if transaction_type not in grouped_data:

            grouped_data[transaction_type] = []


        if amount is not None:

            grouped_data[transaction_type].append(
                float(amount)
            )


    # =========================================
    # PREPARE CHART DATA
    # =========================================

    data = []

    for transaction_type, amounts in grouped_data.items():

        if not amounts:
            continue

        data.append({

            "type": transaction_type,

            "amounts": amounts

        })


    # =========================================
    # SORT BY TOTAL FRAUD AMOUNT
    # =========================================

    data.sort(
        key=lambda item: sum(item["amounts"]),
        reverse=True
    )


    return data


def get_sunburst_chart_data():

    # =========================================
    # TOTAL TRANSACTIONS
    # =========================================

    total_transactions = Transaction.objects.count()

    if total_transactions == 0:
        return {
            "labels": [],
            "parents": [],
            "values": []
        }


    # =========================================
    # NODE ARRAYS
    # =========================================

    labels = [
        "All Transactions"
    ]

    parents = [
        ""
    ]

    values = [
        total_transactions
    ]


    # =========================================
    # TRANSACTION TYPE DATA
    # =========================================

    transaction_types = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            total=Count("id"),
            fraud=Count(
                "id",
                filter=Q(is_fraud=True)
            ),
            safe=Count(
                "id",
                filter=Q(is_fraud=False)
            )
        )
        .order_by("-total")
    )


    # =========================================
    # BUILD HIERARCHY
    # =========================================

    for row in transaction_types:

        transaction_type = (
            row["transaction_type"]
        )

        total = row["total"]
        fraud = row["fraud"]
        safe = row["safe"]


        if not transaction_type:
            transaction_type = "Unknown"


        # -------------------------------------
        # TRANSACTION TYPE NODE
        # -------------------------------------

        labels.append(
            transaction_type
        )

        parents.append(
            "All Transactions"
        )

        values.append(
            total
        )


        # -------------------------------------
        # FRAUD NODE
        # -------------------------------------

        if fraud > 0:

            labels.append(
                f"{transaction_type} - Fraud"
            )

            parents.append(
                transaction_type
            )

            values.append(
                fraud
            )


        # -------------------------------------
        # SAFE NODE
        # -------------------------------------

        if safe > 0:

            labels.append(
                f"{transaction_type} - Safe"
            )

            parents.append(
                transaction_type
            )

            values.append(
                safe
            )


    # =========================================
    # RETURN DATA
    # =========================================

    return {
        "labels": labels,
        "parents": parents,
        "values": values
    }




from django.db.models import Sum


def get_fraud_cases():

    cases = (
        FraudCase.objects
        .all()
        .order_by("-detection_time")
    )

    fraud_cases = []

    for case in cases:

        fraud_cases.append({

            "case_id":
                case.case_id,

            "transaction_id":
                case.transaction_id,

            "customer_id":
                case.customer_id,

            "amount":
                float(case.fraud_amount),

            "fraud_type":
                case.fraud_type,

            "status":
                case.status,

            "detection_time":
                case.detection_time.strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "investigator":
                case.investigator,
        })

    # Total fraud cases
    total_fraud_cases = FraudCase.objects.count()

    # Total fraud amount
    fraud_amount = (
        FraudCase.objects.aggregate(
            total=Sum("fraud_amount")
        )["total"] or 0
    )

    fraud_amount = float(fraud_amount)

    # Convert fraud amount to Cr / Lakh / K
    if fraud_amount >= 1_00_00_000:
        fraud_amount_display = f"₹{fraud_amount / 1_00_00_000:.2f} Cr"

    elif fraud_amount >= 1_00_000:
        fraud_amount_display = f"₹{fraud_amount / 1_00_000:.2f} Lakh"

    elif fraud_amount >= 1_000:
        fraud_amount_display = f"₹{fraud_amount / 1_000:.2f}K"

    else:
        fraud_amount_display = f"₹{fraud_amount:,.0f}"

    # Confirmed cases
    confirmed_cases = FraudCase.objects.filter(
        status__iexact="Confirmed"
    ).count()

    # Under Review cases
    under_review_cases = FraudCase.objects.filter(
        status__iexact="Under Review"
    ).count()

    # False Positive cases
    false_positive_cases = FraudCase.objects.filter(
        status__iexact="False Positive"
    ).count()

    return {
        "cases": fraud_cases,
        "fraud_amount": fraud_amount_display,
        "total_fraud_cases": total_fraud_cases,
        "confirmed_cases": confirmed_cases,
        "under_review_cases": under_review_cases,
        "false_positive_cases": false_positive_cases,
    }




def get_pattern_distribution_data():

    data = (
        Alert.objects
        .values("alert_type")
        .annotate(
            count=Count("alert_id")
        )
        .order_by("-count")
    )

    labels = []
    values = []

    for row in data:

        pattern = (
            row["alert_type"]
            or "Unknown"
        )

        labels.append(pattern)
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



    return result

def get_pattern_trend_data():

    data = (
        Alert.objects
        .annotate(
            date=TruncDate("timestamp")
        )
        .values("date")
        .annotate(
            count=Count("alert_id")
        )
        .order_by("date")
    )

    dates = []
    counts = []

    for row in data:

        if row["date"] is None:
            continue

        dates.append(
            row["date"].strftime("%d %b %Y")
        )

        counts.append(
            row["count"]
        )

    result = {
        "dates": dates,
        "counts": counts
    }



    return result

def get_severity_data():

    severity_order = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    data = (
        Alert.objects
        .values("severity")
        .annotate(
            count=Count("alert_id")
        )
    )

    count_map = {}

    for row in data:

        severity = (
            row["severity"] or "Unknown"
        )

        count_map[severity.lower()] = row["count"]

    labels = []
    values = []

    for severity in severity_order:

        labels.append(severity)

        values.append(
            count_map.get(
                severity.lower(),
                0
            )
        )

    colors = [
        "#00D4AA",   # Low
        "#FFB432",   # Medium
        "#FF8A8A",   # High
        "#FF6B6B"    # Critical
    ]

    result = {
        "labels": labels,
        "values": values,
        "colors": colors
    }

    print("\n====================================")
    print("SEVERITY DATA")
    print("DATA:", result)
    print("====================================\n")

    return result

def get_segment_pattern_data():

    customers = CustomerProfile.objects.values(
        "customer_id",
        "segment"
    )

    alerts = Alert.objects.values(
        "customer_id",
        "alert_type"
    )

    customer_segments = {
        customer["customer_id"]: customer["segment"] or "Unknown"
        for customer in customers
    }

    result = {}

    for alert in alerts:

        customer_id = alert["customer_id"]
        pattern = alert["alert_type"] or "Unknown"

        segment = customer_segments.get(
            customer_id,
            "Unknown"
        )

        if segment not in result:
            result[segment] = 0

        result[segment] += 1

    # Create labels and values
    labels = []
    values = []

    for segment, count in result.items():
        labels.append(segment)
        values.append(count)

    colors = [
        "#6C3CE1",
        "#00D4AA",
        "#FFB432",
        "#FF6B6B",
        "#8B6FE8",
        "#7A7A9A"
    ]

    return {
        "labels": labels,
        "values": values,
        "colors": [
            colors[i % len(colors)]
            for i in range(len(labels))
        ]
    }


def get_heatmap_data():

    # Initialize 7 days × 24 hours
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    hours = list(range(24))

    # Create empty matrix
    heatmap = {
        day: [0] * 24
        for day in days
    }

    alerts = Alert.objects.values(
        "timestamp"
    )

    for alert in alerts:

        timestamp = alert["timestamp"]

        if not timestamp:
            continue

        hour = timestamp.hour
        day = timestamp.strftime("%A")

        heatmap[day][hour] += 1

    z = [
        heatmap[day]
        for day in days
    ]

    return {
        "x": hours,
        "y": days,
        "z": z
    }


def get_segment_pattern_data():

    customers = CustomerProfile.objects.values(
        "customer_id",
        "segment"
    )

    alerts = Alert.objects.values(
        "customer_id",
        "alert_type"
    )

    customer_segment_map = {
        customer["customer_id"]: customer["segment"] or "Unknown"
        for customer in customers
    }

    segment_data = {}

    for alert in alerts:

        customer_id = alert["customer_id"]
        segment = customer_segment_map.get(
            customer_id,
            "Unknown"
        )

        if segment not in segment_data:
            segment_data[segment] = 0

        segment_data[segment] += 1

    labels = []
    values = []

    for segment, count in segment_data.items():
        labels.append(segment)
        values.append(count)

    colors = [
        "#6C3CE1",
        "#00D4AA",
        "#FFB432",
        "#FF6B6B",
        "#8B6FE8",
        "#7A7A9A"
    ]

    return {
        "labels": labels,
        "values": values,
        "colors": [
            colors[i % len(colors)]
            for i in range(len(labels))
        ]
    }