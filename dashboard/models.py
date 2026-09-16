from django.db import models


class Transaction(models.Model):

    transaction_id = models.CharField(max_length=100, unique=True)
    customer_id = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    timestamp = models.DateTimeField()

    hour = models.IntegerField()
    day_of_week = models.IntegerField()

    location = models.CharField(max_length=100)
    merchant_category = models.CharField(max_length=100)

    is_new_device = models.BooleanField(default=False)

    device_id = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()

    is_fraud = models.BooleanField(default=False)

    transaction_type = models.CharField(max_length=50)
    card_present = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class FraudCase(models.Model):

    # ==========================================
    # CASE INFORMATION
    # ==========================================

    case_id = models.CharField(
        max_length=100,
        unique=True
    )

    transaction_id = models.CharField(
        max_length=100
    )

    customer_id = models.CharField(
        max_length=100
    )

    fraud_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    detection_time = models.DateTimeField()

    fraud_type = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=50
    )

    investigator = models.CharField(
        max_length=150
    )

    def __str__(self):
        return self.case_id


class CustomerProfile(models.Model):

    customer_id = models.CharField(
        max_length=100,
        unique=True
    )

    segment = models.CharField(
        max_length=100
    )

    account_age_days = models.IntegerField()

    risk_score = models.FloatField()

    email_verified = models.BooleanField()

    phone_verified = models.BooleanField()

    avg_monthly_transactions = models.FloatField()

    avg_transaction_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    device_count = models.IntegerField()

    location = models.CharField(
        max_length=150
    )

    def __str__(self):
        return self.customer_id

class Alert(models.Model):

    alert_id = models.CharField(
        max_length=100,
        unique=True
    )

    transaction_id = models.CharField(
        max_length=100
    )

    customer_id = models.CharField(
        max_length=100
    )

    alert_type = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=50
    )

    timestamp = models.DateTimeField()

    is_resolved = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.alert_id