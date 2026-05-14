def calculate_budget(
    total_budget,
    hotel_cost,
    flight_cost
):

    total_expense = hotel_cost + flight_cost

    remaining = total_budget - total_expense

    return {
        "expense": total_expense,
        "remaining": remaining
    }