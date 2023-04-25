DATABASE = {
    "metals": [
        {
            "id": 1,
            "metal": "Sterling Silver",
            "price": 12.42
        },
        {
            "id": 2,
            "metal": "14K Gold",
            "price": 736.4
        },
        {
            "id": 3,
            "metal": "24K Gold",
            "price": 1258.9
        },
        {
            "id": 4,
            "metal": "Platinum",
            "price": 795.45
        },
        {
            "id": 5,
            "metal": "Palladium",
            "price": 1241
        }
    ],
    "sizes": [
        {
            "id": 1,
            "carets": 0.5,
            "price": 405
        },
        {
            "id": 2,
            "carets": 0.75,
            "price": 782
        },
        {
            "id": 3,
            "carets": 1,
            "price": 1470
        },
        {
            "id": 4,
            "carets": 1.5,
            "price": 1997
        },
        {
            "id": 5,
            "carets": 2,
            "price": 3638
        }
    ],
    "styles": [
        {
            "id": 1,
            "style": "Classic",
            "price": 500
        },
        {
            "id": 2,
            "style": "Modern",
            "price": 710
        },
        {
            "id": 3,
            "style": "Vintage",
            "price": 965
        }
    ],
    "orders": [

        {
            "id": 1,
            "metal_id": 3,
            "size_id": 2,
            "style_id": 3,
            "timestamp": 1614659931693
        }
    ]
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id, query_params):
    """For GET requests to a single resource"""
    requested_data = None

    for item in DATABASE[resource]:
        if item["id"] == id:
            requested_data = item
            if resource == "orders":
                if "metal" in query_params["_expand"]:
                    requested_data["metal"] = retrieve("metals", requested_data["metal_id"], query_params)
                if "style" in query_params["_expand"]:
                    requested_data["style"] = retrieve("style", requested_data["style_id"], query_params)
                if "size" in query_params["_expand"]:
                    requested_data["size"] = retrieve("size", requested_data["size_id"], query_params)
    return requested_data


def create(resource, post_body):
    """For POST requests to a collection"""
    max_id = DATABASE[resource][-1]["id"]

    new_id = max_id + 1
    post_body["id"] = new_id

    DATABASE[resource].append(post_body)

    return resource


def update(resource, id, post_body):
    """For PUT requests to a single resource"""
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            DATABASE[resource][index] = post_body
            break


def delete(resource, id):
    """For DELETE requests to a single resource"""
    resource_index = -1
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            resource_index = index

    if resource_index >= 0:
        DATABASE[resource].pop(resource_index)
