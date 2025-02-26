from agents.APIcalls import get_product_search, get_pricing, get_store_locations, get_product_details, get_store_details
from agents.chatAgent import get_response
# from APIcalls import get_product_search, get_pricing, get_store_locations, get_product_details, get_store_details
# from chatAgent import get_response

# Utilities available to the function call agent


def get_item_code(query: str):
    response = get_product_search(query, 1)
    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not find the item code for this item.")
    else:
        return(response[1]["items"][0]["part_number"])


# Get pricing
def get_pricing_util(item: str, need_item_code: bool, unit="EA"):
    if need_item_code:
        item_code = get_item_code(item)
    else:
        item_code = item
    response = get_pricing(item_code, unit)

    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not get pricing for this item.")
    else:
        return("The price of the item is: " + str(response[1]["items"][0]["price"]) + "/" + unit)
    
# print(get_pricing_util("LZA406103A", "EA"))


# Get availability
def get_availability_util(item: str, need_item_code: bool, unit="EA"):

    # Get item code if necessary
    if need_item_code:
        item_code = get_item_code(item)
    else:
        item_code = item

    # Get pricing
    response = get_pricing(item_code, unit)
    print(response)

    # Handle response error
    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not get availability for this item.")
    else:
        if response[1]['items'][0]['in_stock']:
            return("This item is in stock, with " + str(response[1]['items'][0]["available_quantity"]) + " units available.")
        else:
            return("Sorry, item " + item_code + " is out of stock at the moment. We apologize for the inconvenience.")


# Get hours
def get_hours_util(store_id: int):

    store_details = get_store_details(store_id)
    if store_details[1] == "Error":
        return("Sorry, could not get store hours for this store. Please try again later. Error code: " + str(store_details[0]))
    else:
        lat = store_details[1]["location"]['latitude']
        long = store_details[1]["location"]['longitude']

    response = get_store_locations(lat, long, page_size=1)

    hours = response[1]['stores'][0]['hours']

    # Handle response error
    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not get store hours for this store")
    else:
        str = "The hours are:"
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            if day in hours:
                if hours[day]['open'] and hours[day]['close']:
                    line = "\n" + day + "- " + hours[day]['open'] + " to " + hours[day]['close']
                    str += line
                else:
                    str += "\n" + day + "- closed"

        return(str)


# Get an image
def get_image_util(item: str, need_item_code: bool):
    
    # Get item code if necessary
    if need_item_code:
        item_code = get_item_code(item)
    else:
        item_code = item

    # Call get_product_details
    response = get_product_details(item_code)
    print(response)
    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not get an image of this product", None)
    else:
        # TODO: Figure out how to handle images
        image_url = response[1]["image_url"]
        print(image_url)
        return(("Here is an image of the product: ...", image_url))
    

# Use of a part
def use_part_util(item: str, user_input: str, need_item_code: bool):

    # Get item code if necessary
    if need_item_code:
        item_code = get_item_code(item)
    else:
        item_code = item

    response = get_product_details(item_code)
    print(response)
    if response[1] == "Error":
        print("Error: " + str(response[0]))
        return("Sorry, could not get product details", None)
    else:
        product_name = response[1]['product_name']
        description = response[1]['description']

        chat_response = get_response(user_input, "You are a helpful assistant. Explain how to use the specified part", "Product: " + product_name + " Description: " + description)
        return(chat_response)
    
