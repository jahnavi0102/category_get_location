import requests

access_token = "pk.eyJ1IjoiamFobmF2aWphaW4iLCJhIjoiY2xtMzc3eTQ4MmI0aDNkczY0YWI3YnpuZCJ9.lpSDlnxyd3vd28r1YdvfEg"

def get_category():
    """
    Get categories in which we can get locations of different places throught India.
    """
    url = f'https://api.mapbox.com/search/searchbox/v1/list/category?&access_token={access_token}'
    response = requests.get(url)
    data = response.json()
    i = 0
    categories = ""
    count = 0

    #  max 20 categories available.
    for datas in data["listItems"]:
        if count>20:
            break
        categories+=datas["canonical_id"].lower() +","
        count+=1
       
    return categories


def get_locations(category):
    """
    Get Names, Address of different categories in different locations.
    """

    url = f"https://api.mapbox.com/search/searchbox/v1/category/{category}"


    # Define the query parameters as a dictionary
    params = {
        "access_token": access_token,  # Replace with your actual Mapbox access token
        "language": "en",
        "limit": 5,
        "proximity": "77.2274,28.6139",
        "bbox": "68.1866,6.7549,97.3956,35.6745",    #currently set to India only but can be done for variety of places
    }

    # Send a GET request to the URL with the parameters
    response = requests.get(url, params=params)

    #  Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Process the response data here
    else:
        return None

    loc_lists = ""
    for datas in data["features"]:
        loc_lists += f'Name: {datas["properties"]["name"]}, Address: {datas["properties"]["full_address"]}' + " ;"
    
    return loc_lists
    