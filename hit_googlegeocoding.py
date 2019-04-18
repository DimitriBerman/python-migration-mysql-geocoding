import googlemaps
from datetime import datetime

def inject_coordinates_from_google_maps(GOOGLE_MAPS_API_KEY, addresses):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    coordinates = []
    for address in addresses:
        address_for_gmaps = address["address"]
        if address_for_gmaps is None: continue

        print("Intentando Geolocalizar ->")
        print(address)
        
        geocode_result = gmaps.geocode(address_for_gmaps)

        if len(geocode_result) <= 0:
            print("ERROR: Direccion no Encontrada")
            continue
        coordinate = {}
        coordinate["user_meta"] = address
        coordinate["user_id"] = address["user_id"]
        coordinate["latitude"] = geocode_result[0].get('geometry').get('location').get('lat')
        coordinate["longitude"] = geocode_result[0].get('geometry').get('location').get('lng')
        coordinates.append(coordinate)
    return coordinates