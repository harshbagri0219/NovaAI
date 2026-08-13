def analyze_results(results):

    if not results:
        return None

    battery_result = None
    storage_result = None

    for item in results:

        task = item.get("task")
        result = item.get("result")

        if task == "battery":
            battery_result = result

        elif task == "storage":
            storage_result = result

    response = []

    # -----------------------------
    # Battery
    # -----------------------------
    if battery_result:
        response.append(f"Battery: {battery_result}")

    # -----------------------------
    # Storage
    # -----------------------------
    if storage_result:
        response.append(f"Storage:\n{storage_result}")

    # -----------------------------
    # Basic analysis
    # -----------------------------
    if battery_result and storage_result:

        response.append(
            "Overall device status: battery and storage information "
            "have been checked successfully."
        )

    elif battery_result:

        response.append(
            "Battery information has been checked successfully."
        )

    elif storage_result:

        response.append(
            "Storage information has been checked successfully."
        )

    return "\n".join(response)
