import re
from pathlib import Path
import joblib
from django.conf import settings
import pandas as pd
from django.db.models import Q
from django.db.models.aggregates import Sum, Avg, Count, Min, StdDev, Max
from django.db.models.functions import TruncDate
from sklearn.preprocessing import LabelEncoder
import numpy as np
from dashboard.models import Transaction, Alert, CustomerProfile, FraudCase
from django.utils import timezone
from datetime import timedelta

MODEL_PATH = (Path(settings.BASE_DIR) / "models" / "random_forest_new.pkl")


def get_case_id():
    last_case = FraudCase.objects.order_by("-id").first()

    if last_case and last_case.case_id:

        # FC_000129 → 000129
        last_number = int(
            last_case.case_id.split("_")[1]
        )

        next_number = last_number + 1

    else:
        next_number = 1

    return f"FC_{next_number:06d}"

def get_alert_id():
    alerts = Alert.objects.values_list("alert_id", flat=True)

    max_number = 0

    for alert_id in alerts:
        match = re.match(r"ALT_(\d+)$", alert_id)

        if match:
            number = int(match.group(1))
            max_number = max(max_number, number)

    return f"ALT_{max_number + 1:06d}"
# def create_features(new_df, historical_df):
#
#     new_df = new_df.copy()
#     historical_df = historical_df.copy()
#
#     # ==========================================
#     # CONVERT AMOUNT
#     # ==========================================
#
#     new_df["amount"] = pd.to_numeric(
#         new_df["amount"],
#         errors="coerce"
#     ).astype(float)
#
#     historical_df["amount"] = pd.to_numeric(
#         historical_df["amount"],
#         errors="coerce"
#     ).astype(float)
#
#
#     # ==========================================
#     # TIME FEATURES
#     # ==========================================
#
#     new_df["timestamp"] = pd.to_datetime(
#         new_df["timestamp"]
#     )
#
#     new_df["transaction_hour"] = (
#         new_df["timestamp"].dt.hour
#     )
#
#     new_df["transaction_day"] = (
#         new_df["timestamp"].dt.day
#     )
#
#     new_df["transaction_month"] = (
#         new_df["timestamp"].dt.month
#     )
#
#     new_df["transaction_weekday"] = (
#         new_df["timestamp"].dt.weekday
#     )
#
#
#     # =========================================================
#     # 2. CUSTOMER FEATURES
#     # =========================================================
#
#     customer_id = new_df.iloc[0]["customer_id"]
#
#     customer_history = historical_df[
#         historical_df["customer_id"] == customer_id
#     ]
#
#     new_df["customer_transaction_count"] = len(
#         customer_history
#     )
#
#
#     if len(customer_history) > 0:
#
#         new_df["customer_avg_amount"] = (
#             customer_history["amount"].mean()
#         )
#
#         new_df["customer_std_amount"] = (
#             customer_history["amount"].std()
#         )
#
#         new_df["customer_max_amount"] = (
#             customer_history["amount"].max()
#         )
#
#     else:
#
#         new_df["customer_avg_amount"] = 0
#         new_df["customer_std_amount"] = 0
#         new_df["customer_max_amount"] = 0
#
#
#     # =========================================================
#     # 3. AMOUNT RATIO FEATURES
#     # =========================================================
#
#     avg_amount = new_df["customer_avg_amount"].replace(
#         0, 1
#     )
#
#     max_amount = new_df["customer_max_amount"].replace(
#         0, 1
#     )
#
#     new_df["amount_ratio_to_avg"] = (
#         new_df["amount"] / avg_amount
#     )
#
#     new_df["amount_ratio_to_max"] = (
#         new_df["amount"] / max_amount
#     )
#
#
#     # =========================================================
#     # 4. CUSTOMER RECENT TRANSACTIONS
#     # =========================================================
#
#     if len(customer_history) > 0:
#
#         customer_history = customer_history.sort_values(
#             "timestamp"
#         )
#
#         last_5 = customer_history.tail(5)
#
#         new_df["rolling_avg_amount"] = (
#             last_5["amount"].mean()
#         )
#
#         new_df["rolling_std_amount"] = (
#             last_5["amount"].std()
#         )
#
#     else:
#
#         new_df["rolling_avg_amount"] = 0
#         new_df["rolling_std_amount"] = 0
#
#
#     # =========================================================
#     # 5. DEVICE FEATURES
#     # =========================================================
#
#     device_id = new_df.iloc[0]["device_id"]
#
#     device_history = historical_df[
#         historical_df["device_id"] == device_id
#     ]
#
#     new_df["device_total_count"] = len(
#         device_history
#     )
#
#
#     if (
#         "is_fraud" in historical_df.columns
#         and len(device_history) > 0
#     ):
#
#         new_df["device_fraud_count"] = (
#             device_history["is_fraud"].sum()
#         )
#
#         new_df["device_fraud_rate"] = (
#             new_df["device_fraud_count"]
#             / new_df["device_total_count"]
#         )
#
#     else:
#
#         new_df["device_fraud_count"] = 0
#         new_df["device_fraud_rate"] = 0
#
#
#     # =========================================================
#     # 6. LOCATION FEATURES
#     # =========================================================
#
#     location = new_df.iloc[0]["location"]
#
#     location_history = historical_df[
#         historical_df["location"] == location
#     ]
#
#     new_df["location_total_count"] = len(
#         location_history
#     )
#
#
#     if (
#         "is_fraud" in historical_df.columns
#         and len(location_history) > 0
#     ):
#
#         new_df["location_fraud_count"] = (
#             location_history["is_fraud"].sum()
#         )
#
#         new_df["location_fraud_rate"] = (
#             new_df["location_fraud_count"]
#             / new_df["location_total_count"]
#         )
#
#     else:
#
#         new_df["location_fraud_count"] = 0
#         new_df["location_fraud_rate"] = 0
#
#
#     # =========================================================
#     # 7. NEW DEVICE FEATURE
#     # =========================================================
#
#     new_df["is_new_device"] = new_df[
#         "is_new_device"
#     ].astype(int)
#
#
#     # =========================================================
#     # 8. CARD PRESENT
#     # =========================================================
#
#     new_df["card_present"] = new_df[
#         "card_present"
#     ].astype(int)
#
#
#     # =========================================================
#     # 9. CLEAN MISSING VALUES
#     # =========================================================
#
#     new_df = new_df.fillna(0)
#
#
#     # =========================================================
#     # 10. PRINT RESULT
#     # =========================================================
#
#     print("\n========================================")
#     print("       ENGINEERED FEATURE DATA")
#     print("========================================")
#
#     print(new_df.to_string(index=False))
#
#     print("\n========================================")
#     print("FEATURE COLUMNS")
#     print("========================================")
#
#     for column in new_df.columns:
#         print(column)
#
#     print("========================================\n")
#
#
#     return new_df

def predict_fraud(engineered_df):
    """
    Takes engineered transaction data
    and returns Random Forest prediction.
    """

    # ==========================================
    # 1. LOAD TRAINED RANDOM FOREST MODEL
    # ==========================================

    random_forest_model = joblib.load(MODEL_PATH)

    print("\n" + "=" * 70)
    print("RANDOM FOREST MODEL LOADED")
    print("=" * 70)

    print("Model path:", MODEL_PATH)

    # ==========================================
    # 2. GET EXACT FEATURES USED DURING TRAINING
    # ==========================================

    model_features = (
        random_forest_model.feature_names_in_.tolist()
    )

    print("\n" + "=" * 70)
    print("FEATURES USED DURING RANDOM FOREST TRAINING")
    print("=" * 70)

    for i, feature in enumerate(model_features, start=1):
        print(f"{i:2}. {feature}")

    # ==========================================
    # 3. CHECK WHICH FEATURES ARE MISSING
    # ==========================================

    missing_features = [
        feature
        for feature in model_features
        if feature not in engineered_df.columns
    ]

    print("\n" + "=" * 70)
    print("MISSING FEATURES")
    print("=" * 70)

    if missing_features:

        for feature in missing_features:
            print("MISSING:", feature)

        raise ValueError(
            f"Missing features required by Random Forest: "
            f"{missing_features}"
        )

    else:

        print("No missing features.")

    # ==========================================
    # 4. CHECK EXTRA FEATURES
    # ==========================================

    extra_features = [
        feature
        for feature in engineered_df.columns
        if feature not in model_features
    ]

    print("\n" + "=" * 70)
    print("EXTRA FEATURES")
    print("=" * 70)

    if extra_features:

        for feature in extra_features:
            print("EXTRA:", feature)

    else:

        print("No extra features.")

    # ==========================================
    # 5. SELECT EXACT MODEL FEATURES
    # ==========================================

    X = engineered_df[model_features].copy()

    # ==========================================
    # 6. CONVERT DATA TO NUMERIC
    # ==========================================

    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # ==========================================
    # 7. HANDLE MISSING VALUES
    # ==========================================

    X = X.fillna(0)

    # ==========================================
    # 8. CHECK FINAL MODEL INPUT
    # ==========================================

    print("\n" + "=" * 70)
    print("FINAL DATA SENT TO RANDOM FOREST")
    print("=" * 70)

    print(X.to_string(index=False))

    print("\n" + "=" * 70)
    print("FINAL FEATURE ORDER")
    print("=" * 70)

    for i, feature in enumerate(X.columns, start=1):
        print(f"{i:2}. {feature}")

    # ==========================================
    # 9. CHECK SHAPE
    # ==========================================

    print("\n" + "=" * 70)
    print("MODEL INPUT SHAPE")
    print("=" * 70)

    print("Rows    :", X.shape[0])
    print("Columns :", X.shape[1])

    print("=" * 70)

    # ==========================================
    # 10. RANDOM FOREST PREDICTION
    # ==========================================

    prediction = random_forest_model.predict(X)

    # ==========================================
    # 11. FRAUD PROBABILITY
    # ==========================================

    probability = (
        random_forest_model.predict_proba(X)
    )

    # Probability of class 1 = Fraud
    fraud_probability = float(
        probability[0][1]
    )

    # ==========================================
    # 12. PREDICTION VALUE
    # ==========================================

    prediction_value = int(
        prediction[0]
    )

    # ==========================================
    # 13. FRAUD STATUS
    # ==========================================

    if prediction_value == 1:

        fraud_status = "Fraud"

    else:

        fraud_status = "Not Fraud"

    # ==========================================
    # 14. CREATE RESULT
    # ==========================================

    result = {

        "prediction":
            prediction_value,

        "fraud_status":
            fraud_status,

        "fraud_probability":
            round(
                fraud_probability,
                4
            ),

        "fraud_percentage":
            round(
                fraud_probability * 100,
                2
            )
    }

    # ==========================================
    # 15. PRINT RESULT
    # ==========================================

    print("\n" + "=" * 70)
    print("             RANDOM FOREST RESULT")
    print("=" * 70)

    print(
        "Prediction        :",
        prediction_value
    )

    print(
        "Fraud Status      :",
        fraud_status
    )

    print(
        "Fraud Probability :",
        round(
            fraud_probability,
            4
        )
    )

    print(
        "Fraud Percentage  :",
        f"{fraud_probability * 100:.2f}%"
    )

    print("=" * 70)

    # ==========================================
    # 16. RETURN RESULT
    # ==========================================

    return result


def create_features(engineered_df):
    """Create engineered features for fraud detection"""

    df = engineered_df.copy()
    timestamp = pd.Timestamp.now()
    new_df = pd.DataFrame()

    customer_id = str(
        df["customer_id"].iloc[0]
    ).strip()

    customer = CustomerProfile.objects.filter(
        customer_id=customer_id
    ).first()

    if customer is None:
        raise ValueError(
            f"CustomerProfile not found for customer_id: {customer_id}"
        )

    transactions = Transaction.objects.filter(
        customer_id=customer_id
    )
    transactions_loc = transactions.values_list("location", flat=True)

    transactions_roll = Transaction.objects.filter(
        customer_id=customer_id
    ).order_by("-timestamp")[:5]

    amounts = [float(a) for a in transactions_roll.values_list("amount", flat=True)]


    customer_loc = customer.location

    device_id = df["device_id"].iloc[0]
    location = df["location"].iloc[0]
    device_transactions = Transaction.objects.filter(
        device_id=device_id
    )

    device_fraud_count = device_transactions.filter(
        is_fraud=True
    ).count()

    location_customers = CustomerProfile.objects.filter(
        location=location
    ).values_list("customer_id", flat=True)

    location_transactions = Transaction.objects.filter(
        customer_id__in=location_customers
    )

    location_total_count = location_transactions.count()

    location_fraud_count = location_transactions.filter(
        is_fraud=True
    ).count()

    if location_total_count > 0:
        location_fraud_rate = (
                location_fraud_count / location_total_count
        )
    else:
        location_fraud_rate = 0

    new_df["amount"] = df["amount"]

    new_df["hour"] = [timestamp.hour]

    new_df["day_of_week"] = [timestamp.weekday()]

    new_df["is_new_device"] = df["is_new_device"]

    card_present = df["card_present"].iloc[0]

    new_df["card_present"] = [
        1 if str(card_present).lower() == "yes" else 0
    ]

    new_df["amount_log"] = np.log1p(df["amount"].astype(float))

    new_df["is_weekend"] = (new_df["day_of_week"] >= 5).astype(int)

    new_df["account_age_days"] = [customer.account_age_days]

    if customer:
        new_df["risk_score"] = [customer.risk_score]
    else:
        new_df["risk_score"] = [0.0]

    new_df["email_verified"] = [1 if customer.email_verified else 0]

    new_df["phone_verified"] = [1 if customer.phone_verified else 0]

    new_df["avg_monthly_transactions"] = [customer.avg_monthly_transactions]

    new_df["avg_transaction_amount"] = [customer.avg_transaction_amount]

    new_df["device_count"] = [customer.device_count]

    new_df["transaction_hour"] = [timestamp.hour]
    new_df["transaction_day"] = [timestamp.day]
    new_df["transaction_month"] = [timestamp.month]
    new_df["transaction_weekday"] = [timestamp.weekday()]

    new_df["customer_transaction_count"] = [transactions.count()]

    new_df["customer_avg_amount"] = [float(transactions.aggregate(avg=Avg("amount"))["avg"] or 0)]

    new_df["customer_std_amount"] = [float(transactions.aggregate(std=StdDev("amount"))["std"] or 0)]

    new_df["customer_max_amount"] = [float(transactions.aggregate(max_amount=Max("amount"))["max_amount"] or 0)]

    device_total_count = device_transactions.count()

    new_df["device_total_count"] = [device_total_count]

    new_df["device_fraud_count"] = [device_fraud_count]

    new_df["location_fraud_count"] = [location_fraud_count]

    new_df["location_total_count"] = [location_total_count]

    new_df["location_fraud_rate"] = [location_fraud_rate]
    new_df["location_x"] = [transactions_loc]
    new_df["location_y"] = [customer_loc]
    new_df["location_mismatch"] = (new_df["location_x"] != new_df["location_y"]).astype(int)

    new_df["segment"] = [customer.segment]

    # --- Missing rolling features ---
    if len(amounts) > 0:
        new_df["rolling_avg_amount"] = [float(np.mean(amounts))]
        new_df["rolling_std_amount"] = [float(np.std(amounts))]
    else:
        new_df["rolling_avg_amount"] = [0.0]
        new_df["rolling_std_amount"] = [0.0]

    current_amount = float(df["amount"].iloc[0])
    cust_avg = float(new_df["customer_avg_amount"].iloc[0])
    cust_max = float(new_df["customer_max_amount"].iloc[0])

    new_df["amount_ratio_to_avg"] = [
        current_amount / cust_avg if cust_avg else 0.0
    ]

    new_df["amount_ratio_to_max"] = [
        current_amount / cust_max if cust_max else 0.0
    ]

    new_df["device_fraud_rate"] = [
        device_fraud_count / device_total_count if device_total_count else 0.0
    ]

    new_df["risk_score_amount"] = [
        float(new_df["risk_score"].iloc[0]) * current_amount
    ]

    # --- Encoders ---
    segment_encoder = LabelEncoder()
    merchant_encoder = LabelEncoder()
    transaction_type_encoder = LabelEncoder()
    location_x_encoder = LabelEncoder()
    location_y_encoder = LabelEncoder()

    new_df["segment_encoded"] = segment_encoder.fit_transform(
        new_df["segment"].astype(str)
    )

    new_df["merchant_category_encoded"] = merchant_encoder.fit_transform(
        df["merchant_category"].astype(str)
    )

    new_df["transaction_type_encoded"] = transaction_type_encoder.fit_transform(
        df["transaction_type"].astype(str)
    )

    new_df["location_x_encoded"] = location_x_encoder.fit_transform(
        new_df["location_x"].astype(str)
    )

    new_df["location_y_encoded"] = location_y_encoder.fit_transform(
        new_df["location_y"].astype(str)
    )

    # ==========================================
    # BASIC DATA TYPES
    # ==========================================

    # df["amount"] = pd.to_numeric(df["amount"],errors="coerce").fillna(0)

    # ==========================================
    # DEFAULT COLUMNS
    # Add columns required by feature engineering
    # ==========================================

    # if "is_fraud" not in df.columns:
    #     df["is_fraud"] = 0
    #
    # if "location_x" not in df.columns:
    #     df["location_x"] = df["location"]
    #
    # if "location_y" not in df.columns:
    #     df["location_y"] = df["location"]
    #
    # if "segment" not in df.columns:
    #     df["segment"] = "Unknown"
    #
    # if "risk_score" not in df.columns:
    #     df["risk_score"] = 0
    #
    # if amounts:
    #     rolling_avg = sum(amounts) / len(amounts)
    # else:
    #     rolling_avg = 0
    #
    # new_df["rolling_avg_amount"] = [rolling_avg]
    #
    # if len(amounts) > 1:
    #     rolling_std = np.std(amounts, ddof=1)
    # else:
    #     rolling_std = 0
    #
    # new_df["rolling_std_amount"] = [rolling_std]
    #
    # new_df["amount_ratio_to_avg"] = (
    #         new_df["amount"] /
    #         new_df["customer_avg_amount"].replace(0, 1)
    # )
    #
    # new_df["amount_ratio_to_max"] = (
    #         new_df["amount"] /
    #         new_df["customer_max_amount"].replace(0, 1)
    # )
    #
    # if device_total_count > 0:
    #     device_fraud_rate = (
    #             device_fraud_count /
    #             device_total_count
    #     )
    # else:
    #     device_fraud_rate = 0
    #
    # new_df["device_fraud_rate"] = [device_fraud_rate]




    # ==========================================
    # TIME FEATURES
    # ==========================================

    # df["timestamp"] = pd.to_datetime(
    #     df["timestamp"]
    # )
    #
    # df["transaction_hour"] = (
    #     df["timestamp"].dt.hour
    # )
    #
    # df["transaction_day"] = (
    #     df["timestamp"].dt.day
    # )
    #
    # df["transaction_month"] = (
    #     df["timestamp"].dt.month
    # )
    #
    # df["transaction_weekday"] = (
    #     df["timestamp"].dt.weekday
    # )
    #
    # new_df["location_y"] = [customer.location]
    #
    # new_df["location_mismatch"] = [
    #     int(
    #         new_df["location_x"].iloc[0]
    #         != new_df["location_y"].iloc[0]
    #     )
    # ]
    #
    # new_df["risk_score_amount"] = (
    #         new_df["risk_score"] * new_df["amount"]
    # )
    #
    #
    #
    # # ==========================================
    # # CUSTOMER FEATURES
    # # ==========================================
    #
    # df["customer_transaction_count"] = (
    #     df.groupby("customer_id")["transaction_id"]
    #     .transform("count")
    # )
    #
    # df["customer_avg_amount"] = (
    #     df.groupby("customer_id")["amount"]
    #     .transform("mean")
    # )

    # df["customer_std_amount"] = (
    #     df.groupby("customer_id")["amount"]
    #     .transform("std")
    # )
    #
    # df["customer_max_amount"] = (
    #     df.groupby("customer_id")["amount"]
    #     .transform("max")
    # )

    # ==========================================
    # ROLLING FEATURES
    # ==========================================

    # df["rolling_avg_amount"] = (
    #     df.groupby("customer_id")["amount"]
    #     .transform(
    #         lambda x: x.rolling(
    #             5,
    #             min_periods=1
    #         ).mean()
    #     )
    # )

    # df["rolling_std_amount"] = (
    #     df.groupby("customer_id")["amount"]
    #     .transform(
    #         lambda x: x.rolling(
    #             5,
    #             min_periods=1
    #         ).std()
    #     )
    # )

    # ==========================================
    # AMOUNT RATIO FEATURES
    # ==========================================

    # df["amount_ratio_to_avg"] = (
    #         df["amount"] /
    #         df["customer_avg_amount"].replace(0, 1)
    # )
    #
    # df["amount_ratio_to_max"] = (
    #         df["amount"] /
    #         df["customer_max_amount"].replace(0, 1)
    # )

    # ==========================================
    # DEVICE FEATURES
    # ==========================================

    # df["device_fraud_count"] = (
    #     df.groupby("device_id")["is_fraud"]
    #     .transform("sum")
    # )
    #
    # df["device_total_count"] = (
    #     df.groupby("device_id")["transaction_id"]
    #     .transform("count")
    # )
    #
    # df["device_fraud_rate"] = (
    #         df["device_fraud_count"] /
    #         df["device_total_count"].replace(0, 1)
    # )

    # ==========================================
    # LOCATION FEATURES
    # ==========================================

    # df["location_fraud_count"] = (
    #     df.groupby("location_x")["is_fraud"]
    #     .transform("sum")
    # )
    #
    # df["location_total_count"] = (
    #     df.groupby("location_x")["transaction_id"]
    #     .transform("count")
    # )
    #
    # df["location_fraud_rate"] = (
    #         df["location_fraud_count"] /
    #         df["location_total_count"].replace(0, 1)
    # )

    # ==========================================
    # LOCATION MISMATCH
    # ==========================================

    # df["location_mismatch"] = (
    #         df["location_x"] != df["location_y"]
    # ).astype(int)

    # ==========================================
    # RISK SCORE INTERACTION
    # ==========================================

    # df["risk_score_amount"] = (
    #         df["risk_score"] *
    #         df["amount"]
    # )

    # ==========================================
    # ADDITIONAL FEATURES REQUIRED BY MODEL
    # ==========================================

    # df["amount_log"] = np.log1p(
    #     df["amount"]
    # )

    # df["is_weekend"] = (
    #         df["transaction_weekday"] >= 5
    # ).astype(int)
    #
    # if "account_age_days" not in df.columns:
    #     df["account_age_days"] = 0
    #
    # if "email_verified" not in df.columns:
    #     df["email_verified"] = 0
    #
    # if "phone_verified" not in df.columns:
    #     df["phone_verified"] = 0
    #
    # if "avg_monthly_transactions" not in df.columns:
    #     df["avg_monthly_transactions"] = 0
    #
    # if "avg_transaction_amount" not in df.columns:
    #     df["avg_transaction_amount"] = (
    #         df["customer_avg_amount"]
    #     )
    #
    # if "device_count" not in df.columns:
    #     df["device_count"] = (
    #         df["device_total_count"]
    #     )

    # ==========================================
    # CATEGORICAL ENCODING
    # ==========================================

    # categorical_cols = [
    #
    #     "segment",
    #     "merchant_category",
    #     "transaction_type",
    #     "location_x",
    #     "location_y"
    #
    # ]
    #
    # for col in categorical_cols:
    #     le = LabelEncoder()
    #
    #     df[f"{col}_encoded"] = (
    #         le.fit_transform(
    #             df[col].astype(str)
    #         )
    #     )

    # ==========================================
    # FILL NaN VALUES
    # ==========================================

    # df = df.fillna(0)

    # ==========================================
    # DROP COLUMNS NOT USED BY MODEL
    # ==========================================

    # columns_to_drop = [
    #
    #     "timestamp",
    #     "customer_id",
    #     "transaction_id",
    #     "device_id",
    #     "ip_address",
    #
    #     "is_fraud",
    #
    #     "segment",
    #     "merchant_category",
    #     "transaction_type",
    #     "location_x",
    #     "location_y"
    #
    # ]

    # df = df.drop(
    #     columns=columns_to_drop,
    #     errors="ignore"
    # )

    return new_df


def get_metrics():
    # =========================
    # TOTAL TRANSACTIONS
    # =========================

    total_transaction = Transaction.objects.count()

    # =========================
    # TOTAL AMOUNT
    # =========================

    total_amount = (
            Transaction.objects.aggregate(
                total=Sum("amount")
            )["total"] or 0
    )

    total_amount = float(total_amount)

    if total_amount >= 1_00_00_000:
        total_amount_display = f"₹{total_amount / 1_00_00_000:.2f} Cr"
    elif total_amount >= 1_00_000:
        total_amount_display = f"₹{total_amount / 1_00_000:.2f} Lakh"
    elif total_amount >= 1_000:
        total_amount_display = f"₹{total_amount / 1_000:.2f}K"
    else:
        total_amount_display = f"₹{total_amount:,.0f}"

    # =========================
    # FRAUD DETECTION
    # =========================

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
    # =========================
    # AVERAGE AMOUNT
    # =========================


    average_amount = (
            Transaction.objects.aggregate(
                average=Avg("amount")
            )["average"] or 0
    )

    average_amount = float(average_amount)

    if average_amount >= 1_00_00_000:
        average_amount_display = f"₹{average_amount / 1_00_00_000:.2f} Cr"

    elif average_amount >= 1_00_000:
        average_amount_display = f"₹{average_amount / 1_00_000:.2f} Lakh"

    elif average_amount >= 1_000:
        average_amount_display = f"₹{average_amount / 1_000:.2f}K"

    else:
        average_amount_display = f"₹{average_amount:,.0f}"


    # =========================
    # LAST 90 DAYS
    # =========================

    ninety_days_ago = timezone.now() - timedelta(days=90)

    transaction_volume = list(
        Transaction.objects
        .filter(timestamp__gte=ninety_days_ago)
        .annotate(
            date=TruncDate("timestamp")
        )
        .values("date")
        .annotate(
            total_transactions=Count("id")
        )
        .order_by("date")
    )
    print("TRANSACTION VOLUME:")
    print(transaction_volume)
    # =========================
    # DETECTION RATE
    # =========================

    if total_transaction > 0:
        detection_rate = (
                                 total_fraud / total_transaction
                         ) * 100
    else:
        detection_rate = 0

    # =========================
    # RETURN METRICS
    # =========================

    start_date = Transaction.objects.aggregate(
        min_date=Min("timestamp")
    )["min_date"]

    if start_date:
        start_date = start_date.date()

    daily_amount = (
        Transaction.objects
        .filter(timestamp__date__gte=start_date)
        .annotate(
            date=TruncDate("timestamp")
        )
        .values("date")
        .annotate(
            total_amount=Sum("amount")
        )
        .order_by("date")
    )

    amount_data = {
        item["date"]: item["total_amount"]
        for item in daily_amount
    }

    transaction_amount = []

    for i in range(90):
        date = start_date + timedelta(days=i)

        transaction_amount.append({
            "date": date,
            "total_amount": amount_data.get(date, 0)
        })

    # =====================================================
    # TRANSACTIONS BY TYPE
    # =====================================================

    transactions_by_type = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            total_transactions=Count("id"),
            fraud_transactions=Count(
                "id",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("-total_transactions")
    )

    transaction_type_data = [
        {
            "transaction_type": item["transaction_type"],
            "total_transactions": item["total_transactions"],
            "fraud_transactions": item["fraud_transactions"],
        }
        for item in transactions_by_type
    ]

    amount_distribution = list(
        Transaction.objects.values_list("amount", flat=True)
    )

    amount_distribution = [
        float(amount)
        for amount in amount_distribution
        if amount is not None
    ]

    amount_ranges = [
        {
            "label": "₹0 – ₹1,000",
            "count": Transaction.objects.filter(
                amount__gte=0,
                amount__lte=1000
            ).count()
        },
        {
            "label": "₹1,000 – ₹5,000",
            "count": Transaction.objects.filter(
                amount__gt=1000,
                amount__lte=5000
            ).count()
        },
        {
            "label": "₹5,000 – ₹10,000",
            "count": Transaction.objects.filter(
                amount__gt=5000,
                amount__lte=10000
            ).count()
        },
        {
            "label": "₹10,000 – ₹25,000",
            "count": Transaction.objects.filter(
                amount__gt=10000,
                amount__lte=25000
            ).count()
        },
        {
            "label": "₹25,000 – ₹50,000",
            "count": Transaction.objects.filter(
                amount__gt=25000,
                amount__lte=50000
            ).count()
        },
        {
            "label": "₹50,000+",
            "count": Transaction.objects.filter(
                amount__gt=50000
            ).count()
        }
    ]

    transactions = Transaction.objects.all().order_by("-created_at")[:20]

    print("TRANSACTIONS:", transactions)
    print("COUNT:", transactions.count())

    return {
        "total_transaction": total_transaction,
        "total_amount": total_amount_display,
        "total_fraud": total_fraud,
        "total_safe": total_safe,
        "transactions": transactions,
        "amount_ranges": amount_ranges,
        "average_amount": average_amount_display,
        "detection_rate": round(detection_rate, 2),
        "fraud_rate": fraud_rate,

        # Last 90 days transaction volume
        "transaction_volume": transaction_volume,
        "transaction_amount": transaction_amount,
        'amount_distribution': amount_distribution,

        "transaction_type_data": transaction_type_data,
    }


def get_donut_chart_data():
    fraud = Transaction.objects.filter(
        is_fraud=True
    ).count()

    safe = Transaction.objects.filter(
        is_fraud=False
    ).count()

    return [
        {
            "label": "Safe Transactions",
            "count": safe
        },
        {
            "label": "Fraud Transactions",
            "count": fraud
        }
    ]


def get_top_fraud_locations():
    locations = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("location")
        .annotate(fraud_count=Count("id"))
        .order_by("-fraud_count")[:5]
    )

    return list(locations)


def get_cumulative_growth_data():
    daily_data = (
        Transaction.objects
        .values(date=TruncDate("timestamp"))
        .annotate(
            total=Count("id"),
            fraud=Count(
                "id",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("date")
    )

    dates = []
    total = []
    fraud = []

    cumulative_total = 0
    cumulative_fraud = 0

    for row in daily_data:
        cumulative_total += row["total"]
        cumulative_fraud += row["fraud"]

        dates.append(
            row["date"].strftime("%Y-%m-%d")
        )

        total.append(cumulative_total)
        fraud.append(cumulative_fraud)

    return {
        "dates": dates,
        "total": total,
        "fraud": fraud
    }


def get_transaction_type_comparison():
    transaction_data = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            total=Count("id"),
            fraud=Count(
                "id",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("transaction_type")
    )

    labels = []
    total = []
    fraud = []

    for row in transaction_data:
        labels.append(
            row["transaction_type"]
        )

        total.append(
            row["total"]
        )

        fraud.append(
            row["fraud"]
        )

    return {
        "labels": labels,
        "total": total,
        "fraud": fraud
    }


def get_transaction_amount_comparison():
    transaction_data = (
        Transaction.objects
        .values("transaction_type")
        .annotate(
            total_amount=Sum("amount"),

            fraud_amount=Sum(
                "amount",
                filter=Q(is_fraud=True)
            )
        )
        .order_by("transaction_type")
    )

    data = []

    for row in transaction_data:
        total_amount = row["total_amount"] or 0
        fraud_amount = row["fraud_amount"] or 0

        net_amount = (
                total_amount - fraud_amount
        )

        data.append({
            "transaction_type":
                row["transaction_type"],

            "total_amount":
                float(total_amount),

            "fraud_amount":
                float(fraud_amount),

            "net_amount":
                float(net_amount)
        })

    return data


def get_transaction_history():
    queryset = (
        Transaction.objects
        .all()
        .order_by("-timestamp")[:10000]
    )

    transaction_history = []

    for transaction in queryset:
        transaction_history.append({
            "transaction_id": transaction.transaction_id,
            "customer_id": transaction.customer_id,
            "amount": float(transaction.amount or 0),
            "transaction_type": transaction.transaction_type or "",
            "location": transaction.location or "",
            "is_fraud": bool(transaction.is_fraud),
            "timestamp": (
                transaction.timestamp.strftime(
                    "%d %b %Y, %I:%M %p"
                )
                if transaction.timestamp
                else ""
            ),
        })

    print("====================================")
    print("TRANSACTION HISTORY UTILITY")
    print("COUNT:", len(transaction_history))
    print("FIRST:", transaction_history[:1])
    print("====================================")

    return transaction_history


def get_transaction_by_id(transaction_id):
    """
    Find a transaction using transaction_id.
    """

    try:
        return Transaction.objects.get(
            transaction_id=transaction_id
        )

    except Transaction.DoesNotExist:
        return None

