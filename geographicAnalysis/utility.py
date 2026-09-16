from dashboard.models import Transaction


def get_world_map_data():

    transactions = Transaction.objects.values(
        "location",
        "is_fraud"
    )

    country_data = {}

    for transaction in transactions:

        country = transaction["location"] or "Unknown"
        is_fraud = bool(transaction["is_fraud"])

        if country not in country_data:
            country_data[country] = {
                "total_tx": 0,
                "fraud_tx": 0
            }

        country_data[country]["total_tx"] += 1

        if is_fraud:
            country_data[country]["fraud_tx"] += 1

    result = []

    for country, values in country_data.items():

        total_tx = values["total_tx"]
        fraud_tx = values["fraud_tx"]

        if total_tx > 0:
            fraud_rate = (fraud_tx / total_tx) * 100
        else:
            fraud_rate = 0

        result.append({
            "location": country,
            "fraud_rate": round(fraud_rate, 2),
            "total_tx": total_tx,
            "fraud_tx": fraud_tx
        })

    # Highest fraud rate first
    result.sort(
        key=lambda x: x["fraud_rate"],
        reverse=True
    )

    return result

def get_top_countries_data():

    transactions = Transaction.objects.values(
        "location",
        "is_fraud"
    )

    country_data = {}

    for transaction in transactions:

        country = transaction["location"] or "Unknown"

        if country not in country_data:
            country_data[country] = {
                "total_tx": 0,
                "fraud_tx": 0
            }

        country_data[country]["total_tx"] += 1

        if transaction["is_fraud"]:
            country_data[country]["fraud_tx"] += 1

    result = []

    for country, values in country_data.items():

        total_tx = values["total_tx"]
        fraud_tx = values["fraud_tx"]

        fraud_rate = (
            (fraud_tx / total_tx) * 100
            if total_tx > 0
            else 0
        )

        result.append({
            "location": country,
            "fraud_rate": round(fraud_rate, 2),
            "total_tx": total_tx,
            "fraud_tx": fraud_tx
        })

    result.sort(
        key=lambda x: x["fraud_rate"],
        reverse=True
    )

    return result


def get_region_data():

    # Country → Region mapping
    country_regions = {
        # North America
        "US": "North America",
        "USA": "North America",
        "CA": "North America",
        "CAN": "North America",
        "MX": "North America",
        "MEX": "North America",

        # Europe
        "UK": "Europe",
        "GB": "Europe",
        "GBR": "Europe",
        "DE": "Europe",
        "DEU": "Europe",
        "FR": "Europe",
        "FRA": "Europe",
        "IT": "Europe",
        "ITA": "Europe",
        "ES": "Europe",
        "ESP": "Europe",

        # Asia
        "IN": "Asia",
        "IND": "Asia",
        "CN": "Asia",
        "CHN": "Asia",
        "JP": "Asia",
        "JPN": "Asia",
        "SG": "Asia",
        "SGP": "Asia",
        "RU": "Asia",
        "RUS": "Asia",

        # Africa
        "NG": "Africa",
        "NGA": "Africa",

        # South America
        "BR": "South America",
        "BRA": "South America",

        # Oceania
        "AU": "Oceania",
        "AUS": "Oceania",
    }

    transactions = Transaction.objects.values(
        "location",
        "is_fraud"
    )

    result = {}

    for transaction in transactions:

        location = (
            transaction["location"] or "Unknown"
        )

        location = location.strip().upper()

        region = country_regions.get(
            location,
            "Other"
        )

        if region not in result:
            result[region] = {
                "total_tx": 0,
                "fraud_tx": 0
            }

        result[region]["total_tx"] += 1

        if transaction["is_fraud"]:
            result[region]["fraud_tx"] += 1

    data = []

    for region, values in result.items():

        data.append({
            "region": region,
            "total_tx": values["total_tx"],
            "fraud_tx": values["fraud_tx"]
        })

    return data

def get_location_heatmap_data():

    transactions = Transaction.objects.values(
        "location",
        "is_fraud"
    )

    location_data = {}

    for transaction in transactions:

        location = transaction["location"] or "Unknown"

        if location not in location_data:
            location_data[location] = {
                "total_tx": 0,
                "fraud_tx": 0
            }

        location_data[location]["total_tx"] += 1

        if transaction["is_fraud"]:
            location_data[location]["fraud_tx"] += 1

    result = []

    for location, values in location_data.items():

        total_tx = values["total_tx"]
        fraud_tx = values["fraud_tx"]

        fraud_rate = (
            (fraud_tx / total_tx) * 100
            if total_tx > 0
            else 0
        )

        result.append({
            "location": location,
            "total_tx": total_tx,
            "fraud_tx": fraud_tx,
            "fraud_rate": round(fraud_rate, 2)
        })

    # Highest transaction locations first
    result.sort(
        key=lambda x: x["total_tx"],
        reverse=True
    )

    return result

def get_country_comparison_data():

    transactions = Transaction.objects.values(
        "location",
        "is_fraud"
    )

    country_data = {}

    for transaction in transactions:

        country = transaction["location"] or "Unknown"

        if country not in country_data:
            country_data[country] = {
                "total_tx": 0,
                "fraud_tx": 0,
                "safe_tx": 0
            }

        country_data[country]["total_tx"] += 1

        if transaction["is_fraud"]:
            country_data[country]["fraud_tx"] += 1
        else:
            country_data[country]["safe_tx"] += 1

    result = []

    for country, values in country_data.items():

        result.append({
            "location": country,
            "total_tx": values["total_tx"],
            "fraud_tx": values["fraud_tx"],
            "safe_tx": values["safe_tx"]
        })

    # Highest transaction countries first
    result.sort(
        key=lambda x: x["total_tx"],
        reverse=True
    )

    return result


def geographicData():



    # ==================================================
    # TOTAL LOCATIONS
    # ==================================================

    total_locations = (
        Transaction.objects
        .values("location")
        .exclude(location__isnull=True)
        .exclude(location="")
        .distinct()
        .count()
    )


    # ==================================================
    # TOTAL TRANSACTIONS
    # ==================================================

    total_transactions = (
        Transaction.objects.count()
    )


    # ==================================================
    # FRAUD LOCATIONS
    # ==================================================

    fraud_locations = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("location")
        .exclude(location__isnull=True)
        .exclude(location="")
        .distinct()
        .count()
    )


    # ==================================================
    # SAFE LOCATIONS
    # ==================================================

    safe_locations = (
        Transaction.objects
        .filter(is_fraud=False)
        .values("location")
        .exclude(location__isnull=True)
        .exclude(location="")
        .distinct()
        .count()
    )


    # ==================================================
    # SUSPICIOUS LOCATIONS
    # ==================================================

    # Locations having at least one fraud transaction
    # but not counted as completely safe.
    suspicious_locations = (
        Transaction.objects
        .filter(is_fraud=True)
        .values("location")
        .exclude(location__isnull=True)
        .exclude(location="")
        .distinct()
        .count()
    )


    # ==================================================
    # FRAUD RATE
    # ==================================================

    fraud_transactions = (
        Transaction.objects
        .filter(is_fraud=True)
        .count()
    )


    fraud_rate = 0

    if total_transactions > 0:

        fraud_rate = round(
            (
                fraud_transactions /
                total_transactions
            ) * 100,
            2
        )




    # ==================================================
    # RENDER
    # ==================================================

    result =  {


            "total_locations":
                total_locations,

            "safe_locations":
                safe_locations,

            "fraud_locations":
                fraud_locations,

            "suspicious_locations":
                suspicious_locations,

            "total_transactions":
                total_transactions,

            "fraud_rate":
                fraud_rate,
        }

    return result
