import random

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from dashboard.models import Transaction, Alert, FraudCase
from transaction.utility import  create_features, predict_fraud, get_metrics, get_donut_chart_data, \
    get_top_fraud_locations, get_cumulative_growth_data, get_transaction_type_comparison, \
    get_transaction_amount_comparison, get_transaction_history, get_alert_id, get_transaction_by_id, get_case_id
from utility import send_mail
from transaction.utility import predict_fraud
from datetime import datetime

def transaction(request, full_name):
    return render(request, "transaction/transaction.html", {
        "full_name": full_name
    })


def fraud_detection(request, full_name):

    if request.method == "POST":



        # ==============================
        # 1. GET FORM DATA
        # ==============================

        customer_id = request.POST.get("customer_id")
        customer_name = request.POST.get("customer_name")
        email = request.POST.get("email")
        transaction_id = request.POST.get("transaction_id")
        amount = request.POST.get("amount")
        transaction_type = request.POST.get("transaction_type")
        location = request.POST.get("location")
        merchant_category = request.POST.get("merchant_category")
        timestamp_string = request.POST.get("timestamp")

        timestamp = datetime.strptime(
            timestamp_string,
            "%Y-%m-%d %H:%M:%S"
        )

        if timezone.is_naive(timestamp):
            timestamp = timezone.make_aware(timestamp)
        device_id = request.POST.get("device_id")
        ip_address = request.POST.get("ip_address")
        card_present = request.POST.get("card_present")


        # ==============================
        # 2. CONVERT FORM DATA
        # ==============================

        try:
            amount = float(amount or 0)
        except (TypeError, ValueError):
            amount = 0.0

        try:
            card_present = int(card_present or 0)
        except (TypeError, ValueError):
            card_present = 0


        # ==============================
        # 3. TIMESTAMP
        # ==============================

        timestamp = timestamp

        local_timestamp = timezone.localtime(
            timestamp
        )

        current_hour = local_timestamp.hour


        # ==============================
        # 4. CHECK NEW DEVICE
        # ==============================

        is_new_device = not Transaction.objects.filter(
            customer_id=customer_id,
            device_id=device_id
        ).exists()


        # ==============================
        # 5. GENERATE TRANSACTION ID
        # ==============================

        #transaction_id = get_transaction_id()


        # ==============================
        # 6. DETERMINE ALERT TYPE
        # ==============================

        alert_type = ""


        allowed_locations = [
            "IN",
            "US",
            "UK",
            "SG"
        ]


        if amount > 50000:

            alert_type = "High Amount"

        elif is_new_device:

            alert_type = "New Device"

        elif (current_hour >= 23or current_hour < 6):

            alert_type = "Unusual Time"

        elif location not in allowed_locations:

            alert_type = "Suspicious Location"


        # ==============================
        # 7. BASIC FEATURE DATA
        # ==============================

        feature_data = {

            "customer_id":
                customer_id,

            "transaction_id":
                transaction_id,

            "amount":
                amount,

            "transaction_type":
                transaction_type,

            "location":
                location,

            "merchant_category":
                merchant_category,

            "device_id":
                device_id,

            "ip_address":
                ip_address,

            "card_present":
                card_present,

            "is_new_device":
                int(is_new_device),

            "timestamp":
                timestamp,

            "hour":
                local_timestamp.hour,

            "day_of_week":
                local_timestamp.weekday(),
        }


        # ==============================
        # 8. CREATE DATAFRAME
        # ==============================

        new_df = pd.DataFrame(
            [feature_data]
        )


        # ==============================
        # 9. FEATURE ENGINEERING
        # ==============================

        engineered_df = create_features(
            new_df
        )


        # ==============================
        # 10. FRAUD PREDICTION
        # ==============================

        predict = predict_fraud(
            engineered_df
        )


        prediction = predict["prediction"]

        fraud_status = predict[
            "fraud_status"
        ]

        fraud_probability = predict[
            "fraud_probability"
        ]

        fraud_percentage = predict[
            "fraud_percentage"
        ]



        # ==============================
        # 11. CREATE TRANSACTION
        # ==============================

        # alert = Alert.objects.create(
        #     alert_id=get_alert_id(),
        #     transaction_id=transaction_id,
        #     customer_id=customer_id,
        #     alert_type="Fraudulent Transaction",
        #     severity="HIGH",
        #     timestamp=timezone.now(),
        #     is_resolved=
        # )

        # ==============================
        # 12. CONVERT FRAUD PROBABILITY
        # ==============================

        try:

            fraud_probability = float(
                fraud_probability or 0
            )

        except (
            TypeError,
            ValueError
        ):

            fraud_probability = 0.0


        # ==============================
        # 13. DETERMINE SEVERITY
        # ==============================

        if fraud_probability < 0.25:

            severity = "Low"

        elif fraud_probability < 0.50:

            severity = "Medium"

        elif fraud_probability < 0.75:

            severity = "High"

        else:

            severity = "Critical"


        # ==============================
        # 14. CREATE ALERT
        # ==============================

        if prediction == 1:

            is_resolve = random.choices(
                [True, False],
                weights=[70, 30]
            )[0]

        statuses = [
            "Under Review",
            "Confirmed",
            "False Positive"
        ]

        alert = Alert.objects.create(

            alert_id=
            get_alert_id(),

            transaction_id=
            transaction_id,

            alert_type=
            alert_type,

            customer_id=
            customer_id,

            severity=
            severity,

            is_resolved=
            False,

            timestamp=
            timestamp
        )

        alert.save()

        if bool(prediction):
            FraudCase.objects.create(

                case_id=
                get_case_id(),

                transaction_id=transaction_id,

                customer_id=
                customer_id,

                fraud_amount=
                amount,

                detection_time=
                timestamp,

                fraud_type=
                alert_type,

                status=random.choice(statuses),


                investigator=
                "Unassigned"
            )

        # ==============================
        # 15. SEND EMAIL
        # ==============================

        if prediction == 0:

            subject = (
                "Transaction Successful"
            )


            message = f"""
Hello {customer_id},

Your transaction has been successfully processed.

Transaction Details
-------------------
Transaction ID: {transaction_id}
Amount: ₹{amount}
Transaction Type: {transaction_type}
Merchant Category: {merchant_category}
Location: {location}

Fraud Detection Result
----------------------
Status: Not Fraud
Fraud Probability: {fraud_percentage}%

Your transaction has been verified successfully.

Thank you.
"""


            send_mail(
                subject,
                message,
                "faruqeansari9@gmail.com",
                [email]
            )


        else:

            subject = (
                "⚠ FRAUD ALERT - "
                "Suspicious Transaction Detected"
            )


            message = f"""
Hello {customer_id},

IMPORTANT SECURITY ALERT

Our fraud detection system has detected a potentially
fraudulent transaction.

Transaction Details
-------------------
Transaction ID: {transaction_id}
Amount: ₹{amount}
Transaction Type: {transaction_type}
Merchant Category: {merchant_category}
Location: {location}
Device ID: {device_id}

Fraud Detection Result
----------------------
Status: FRAUD DETECTED
Fraud Probability: {fraud_percentage}%

Alert Type: {alert_type or "Fraud Detected"}
Severity: {severity}

This transaction has been flagged as suspicious.

If you did not initiate this transaction, please contact
your bank or financial service provider immediately.

Please do not share your OTP, PIN, password, or card details
with anyone.

Thank you.
"""


            send_mail(
                subject,
                message,
                "faruqeansari9@gmail.com",
                [email]
            )


        # ==============================
        # 16. RETURN RESULT
        # ==============================

        return render(

            request,

            "transaction/transaction.html",

            {

                "success":
                    True,

                "message": (

                    "Transaction successful "
                    "and confirmation email sent."

                    if prediction == 0

                    else

                    "Fraud detected. "
                    "Fraud alert email sent."
                ),

                "transaction_id":
                    transaction_id,

                "customer_name":
                    customer_name,

                "amount":
                    amount,

                "transaction_type":
                    transaction_type,

                "merchant_category":
                    merchant_category,

                "location":
                    location,

                "timestamp":
                    timestamp,

                "fraud_status":
                    fraud_status,

                "fraud_probability":
                    fraud_percentage,

                "severity":
                    severity,

                "alert_type":
                    alert_type,

                "raw_data":
                    feature_data,

                "engineered_columns":
                    engineered_df.columns.tolist(),

                "engineered_data":
                    engineered_df.iloc[0].to_dict(),

                "full_name":
                    full_name,
            }
        )


    # ==============================
    # GET REQUEST
    # ==============================

    return render(

        request,

        "transaction/transaction.html"
    )



def transaction_history(request, full_name):



    metric = get_metrics()

    transaction_history_data = get_transaction_history()

    return render(
        request,
        "transaction/transaction_history.html",
        {
            "full_name": full_name,
            "metric": metric,
            "transaction_history_data": transaction_history_data,
        }
    )

def transactionAnalytics(request,full_name):
    donut_chart_data = get_donut_chart_data()
    top_fraud_locations = get_top_fraud_locations()
    cumulative_growth_data = (get_cumulative_growth_data())
    transaction_type_data = (
        get_transaction_type_comparison()
    )
    transaction_amount_data = (
        get_transaction_amount_comparison()
    )


    metric = get_metrics()
    return render(
        request,
        "transaction/transaction_analysis.html",{
            "full_name": full_name,
            "donut_chart_data": donut_chart_data,
            "top_fraud_locations": top_fraud_locations,
            "cumulative_growth_data":cumulative_growth_data,
            "transaction_type_data":transaction_type_data,
            "transaction_amount_data":transaction_amount_data,

            "metric":metric,
        }
    )


def get_transaction(request, transaction_id):

    transaction = get_transaction_by_id(transaction_id)

    if transaction is None:

        return JsonResponse({
            "success": False,
            "message": "Transaction not found"
        })


    return JsonResponse({

        "success": True,

        "transaction": {

            "transaction_id": transaction.transaction_id,

            "customer_id": transaction.customer_id,

            "amount": str(transaction.amount),

            "timestamp": transaction.timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "hour": transaction.hour,

            "day_of_week": transaction.day_of_week,

            "location": transaction.location,

            "merchant_category":
                transaction.merchant_category,

            "is_new_device":
                transaction.is_new_device,

            "device_id": transaction.device_id,

            "ip_address": transaction.ip_address,

            "is_fraud":
                transaction.is_fraud,

            "transaction_type":
                transaction.transaction_type,

            "card_present":
                transaction.card_present,

        }

    })