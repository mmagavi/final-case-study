import requests

# HEALTH CHECK
# NO INPUTS
def health_check():
    HEALTH_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/health"
    response = requests.get(HEALTH_URL)
    return response.json()


# AZURE PRODUCT SEARCH API CALL
# PARAMS:
# - `query` (required): Search query
# - `limit` (optional): Maximum number of results (default: 3)

def get_product_search(query: str, limit: int):
    PRODUCT_SEARCH_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/api/products/search?"
    params = {
        "query": query,
        limit: limit
    }
    response = requests.get(PRODUCT_SEARCH_URL, params=params)

    if response.status_code == 200:
        return (response.status_code, response.json())
    else:
        return ((response.status_code, "Error"))

# print(get_product_search("Pool pump", 5))


# PRICING API CALL
# PARAMS:
# ITEM CODE
# UNIT

def get_pricing(item_code: str, unit: str):
    PRICING_API_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/api/pricing"
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    # JSON Payload
    data = {
        "items": [
            {
                "item_code": item_code,
                "unit": unit
            }
        ]
    }
    response = requests.post(PRICING_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return (response.status_code, response.json())
    else:
        return ((response.status_code, "Error"))
    
# print(get_pricing("LZA406103A", "EA"))


# STORE LOCATIONS API CALL
# PARAMS:
# - `latitude` (required): Latitude coordinate
# - `longitude` (required): Longitude coordinate
# - `radius` (optional): Search radius in miles (default: 50)
# - `page_size` (optional): Results per page (default: 10)
# - `page` (optional): Page number (default: 1)

def get_store_locations(lat: float, lon: float, radius=50, page_size=10, page=1):
    STORE_LOCATIONS_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/api/stores/search"
    params = {
        "latitude": lat,
        "longitude": lon,
        "radius": radius,
        "page_size": page_size,
        "page": page
    }

    response = requests.get(STORE_LOCATIONS_URL, params=params)

    if response.status_code == 200:
        return (response.status_code, response.json())
    else:
        return ((response.status_code, "Error"))

# print(get_store_locations(37.7749, -122.4194))


# GET STORE DETAILS
# PARAMS:
# store id
def get_store_details(store_id: int):
    STORE_DETAILS_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/api/stores/"

    response = requests.get(STORE_DETAILS_URL + str(store_id))

    if response.status_code == 200:
        return (response.status_code, response.json())
    else:
        return ((response.status_code, "Error"))
    
# print(get_store_details(726))


# GET PRODUCT DETAILS API CALL
# PARAM:
# PART NUMBER

def get_product_details(item_code: str):
    PRODUCT_DETAILS_URL = "https://candidate-onsite-study-srs-712206638513.us-central1.run.app/api/products"

    response = requests.get(PRODUCT_DETAILS_URL + "/" + item_code)

    if response.status_code == 200:
        return (response.status_code, response.json())
    else:
        return ((response.status_code, "Error"))
    
# print(get_product_details("LZA406103A"))