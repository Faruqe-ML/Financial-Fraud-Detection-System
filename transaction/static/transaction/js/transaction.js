const transactionInput =
        document.getElementById("transactionId");

    let timeout = null;


    transactionInput.addEventListener("input", function () {

        const transactionId = this.value.trim();

        clearTimeout(timeout);


        // Clear fields if Transaction ID is empty

        if (!transactionId) {

            clearTransactionFields();

            return;
        }


        // Wait until user stops typing

        timeout = setTimeout(function () {

            loadTransaction(transactionId);

        }, 500);

    });



    function loadTransaction(transactionId) {

        const status =
            document.getElementById("transactionStatus");


        if (status) {
            status.innerText = "Searching...";
        }


        fetch(
            `/transaction_data/${encodeURIComponent(transactionId)}/`
        )

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "Server returned " + response.status
                );
            }

            return response.json();

        })

        .then(data => {


            if (data.success) {

                const transaction =
                    data.transaction;


                // -----------------------------
                // Customer Information
                // -----------------------------

                document.getElementById(
                    "customerId"
                ).value = transaction.customer_id;


                // -----------------------------
                // Transaction Details
                // -----------------------------

                document.getElementById(
                    "amount"
                ).value = transaction.amount;


                document.getElementById(
                    "transactionType"
                ).value = transaction.transaction_type;


                document.getElementById(
                    "location"
                ).value = transaction.location;


                document.getElementById(
                    "merchantCategory"
                ).value =
                    transaction.merchant_category;

                document.getElementById(
                    "transactionTime"
                ).value = transaction.timestamp.split(".")[0];


                // -----------------------------
                // Device Information
                // -----------------------------

                document.getElementById(
                    "deviceId"
                ).value = transaction.device_id;


                document.getElementById(
                    "ipAddress"
                ).value = transaction.ip_address;


                // -----------------------------
                // Card Present
                // -----------------------------

                document.getElementById(
                    "cardPresent"
                ).value =
                    transaction.card_present ? "1" : "0";


                // -----------------------------
                // Status
                // -----------------------------

                if (status) {

                    status.innerText =
                        "✓ Transaction found";

                    status.style.color = "green";
                }


                // Enable prediction button

                document.getElementById(
                    "predictBtn"
                ).disabled = false;


            } else {

                clearTransactionFields();


                if (status) {

                    status.innerText =
                        "✗ Transaction not found";

                    status.style.color = "red";
                }

            }

        })

        .catch(error => {

            console.error(
                "Transaction lookup error:",
                error
            );


            clearTransactionFields();


            if (status) {

                status.innerText =
                    "Error loading transaction";

                status.style.color = "red";
            }

        });

    }



    function clearTransactionFields() {

        document.getElementById(
            "customerId"
        ).value = "";


        document.getElementById(
            "customerEmail"
        ).value = "";


        document.getElementById(
            "customerPhone"
        ).value = "";


        document.getElementById(
            "amount"
        ).value = "";


        document.getElementById(
            "transactionType"
        ).value = "";


        document.getElementById(
            "location"
        ).value = "";


        document.getElementById(
            "merchantCategory"
        ).value = "";


        document.getElementById(
            "deviceId"
        ).value = "";


        document.getElementById(
            "ipAddress"
        ).value = "";


        document.getElementById(
            "cardPresent"
        ).value = "";


        document.getElementById(
            "predictBtn"
        ).disabled = true;

    }




    function clearTransactionFields() {

        document.getElementById(
            "transaction_type"
        ).value = "";


        document.getElementById(
            "amount"
        ).value = "";


        document.getElementById(
            "customer_id"
        ).value = "";


        document.getElementById(
            "destination_id"
        ).value = "";


        document.getElementById(
            "oldbalanceOrg"
        ).value = "";


        document.getElementById(
            "newbalanceOrig"
        ).value = "";


        document.getElementById(
            "oldbalanceDest"
        ).value = "";


        document.getElementById(
            "newbalanceDest"
        ).value = "";


        document.getElementById(
            "checkFraudBtn"
        ).disabled = true;

    }



    function closeSuccess() {
        const overlay = document.querySelector(".success-overlay");

        if (overlay) {
            overlay.classList.add("closing");

            setTimeout(() => {
                overlay.style.display = "none";
            }, 300);
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        const closeButton = document.querySelector(".success-close");

        if (closeButton) {
            closeButton.addEventListener("click", closeSuccess);
        }
    });