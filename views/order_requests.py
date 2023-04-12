ORDERS = [
    {
            "id": 1,
            "metal_id": 3,
            "size_id": 2,
            "style_id": 3,
            "timestamp": 1614659931693
        }
]

def get_all_orders():
    return ORDERS


# Function with a single parameter
def get_single_order(id):
    # Variable to hold the found metal, if it exists
    requested_order = None

    # Iterate the METALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order

    return requested_order