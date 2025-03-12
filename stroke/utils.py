import requests
import json

def get_nearest_hospitals(latitude, longitude):
    """
    Finds nearby hospitals using Google Places API (New) and fetches contact numbers.
    """
    if not GOOGLE_MAPS_API_KEY:
        return {"error": "Google API Key is missing."}
    
    if not latitude or not longitude:
        return {"error": "Location not provided."}

    places_url = "https://places.googleapis.com/v1/places:searchNearby"
    data = {
        "includedTypes": ["hospital"],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 5000.0  # 5km search radius
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.id,places.internationalPhoneNumber,places.nationalPhoneNumber"
    }

    try:
        response = requests.post(places_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        results = response.json().get("places", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch hospitals: {e}"}

    if not results:
        return {"error": "No hospitals found nearby."}

    hospitals = []
    for result in results:
        hospital_name = result.get("displayName", {}).get("text", "Unknown Hospital")
        place_id = result.get("id")
        contact_Number =  result.get("internationalPhoneNumber")
        
        hospitals.append({
            "displayName": hospital_name,
            "internationalPhoneNumber": contact_Number
        })
    
    return {"places": hospitals}

GOOGLE_MAPS_API_KEY = "AIzaSyAmKiXF-Umfng3qoOXRO4ewMHKz4SKDBUA"
latitude = 10.5250
longitude = 76.2139

hospitals = get_nearest_hospitals(latitude, longitude)
print(hospitals)
