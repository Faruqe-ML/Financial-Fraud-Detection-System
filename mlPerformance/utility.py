from pathlib import Path
import json

def get_performance_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "model_performance.json"
    )

    print("================================")
    print("PERFORMANCE FILE PATH:")
    print(file_path)
    print("FILE EXISTS:", file_path.exists())
    print("================================")

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        print("PERFORMANCE DATA:")
        print(data)
        print("DATA TYPE:", type(data))
        print("DATA LENGTH:", len(data))

        return data

    except Exception as error:
        print("PERFORMANCE DATA ERROR:", error)
        return []

def get_confusion_matrix_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "model_performance.json"
    )

    print("CONFUSION MATRIX FILE:", file_path)
    print("FILE EXISTS:", file_path.exists())

    if not file_path.exists():
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        result = []

        for model in data:

            matrix = model.get(
                "confusion_matrix"
            )

            if not matrix:
                continue

            result.append({

                "model_name":
                    model.get(
                        "Model",
                        "Unknown"
                    ),

                "confusion_matrix":
                    matrix
            })

        print(
            "CONFUSION MATRIX DATA:",
            result
        )

        return result

    except Exception as error:

        print(
            "CONFUSION MATRIX ERROR:",
            error
        )

        return []



def get_roc_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "model_performance.json"
    )

    print("ROC FILE PATH:")
    print(file_path)

    print("FILE EXISTS:")
    print(file_path.exists())

    if not file_path.exists():
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        result = []

        for model in data:

            fpr = model.get(
                "fpr",
                []
            )

            tpr = model.get(
                "tpr",
                []
            )

            if not fpr or not tpr:
                continue

            result.append({

                "model_name":
                    model.get(
                        "Model",
                        "Unknown"
                    ),

                "roc_auc":
                    round(
                        float(
                            model.get(
                                "ROC-AUC",
                                0
                            )
                        ) * 100,
                        2
                    ),

                "fpr":
                    fpr,

                "tpr":
                    tpr

            })

        print("ROC DATA:")
        print(result)

        return result

    except Exception as error:

        print(
            "ROC DATA ERROR:",
            error
        )

        return []


def get_feature_importance_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "model_performance.json"
    )

    print("FEATURE IMPORTANCE FILE PATH:")
    print(file_path)

    print("FILE EXISTS:")
    print(file_path.exists())

    if not file_path.exists():

        print(
            "Model performance file not found."
        )

        return []


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        result = []


        # ==========================================
        # GET FEATURE IMPORTANCE
        # ==========================================

        for model in data:

            model_name = model.get(
                "Model",
                "Unknown"
            )

            feature_importance = model.get(
                "feature_importance",
                []
            )


            if not feature_importance:
                continue


            result.append({

                "model_name":
                    model_name,

                "feature_importance":
                    feature_importance

            })


        print(
            "FEATURE IMPORTANCE DATA:"
        )

        print(result)


        return result


    except Exception as error:

        print(
            "FEATURE IMPORTANCE ERROR:",
            error
        )

        return []