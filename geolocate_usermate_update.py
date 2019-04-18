import mysql_conection as mssqlconn
import pprint
import hit_googlegeocoding as geocoding


mysql_config = {
    'user': 'ctpcba-prod',
    'password': 'NDNkfq5HSFfY1abyonkI',
    'host': 'dragonstone.dirmod.com',
    'database': 'ctpcba_prod_webinstitucional',
    'raise_on_warnings': True
}
GOOGLE_MAPS_API_KEY='AIzaSyAq7Y5pZJppnwtMfqCjHo335o40iyGRSNQ'

pp = pprint.PrettyPrinter(indent=4)

print("START")
print("Reading Metas From MySql")
pp.pprint(mysql_config)

userMetas = mssqlconn.get_user_metas(mysql_config)

# print("User Metas")
# pp.pprint(userMetas)

print("Map UserMetas to Addresses")

def filterAddress(um):
    # if "user_longitud" not in um and "user_latitud" not in um:
    #     return True
    if "user_direccion" in um:
        return True
    return False

def mapAddress(um):
    address = None
    
    if "user_direccion" in um:
       address = um["user_direccion"]
    
    if address and "user_cod_postal" in um:
        if address is not None: address += ', ' 
        address += um["user_cod_postal"]
    
    if address and "user_ubicacion" in um:
        if address is not None: address += ', ' 
        address += ', ' + um["user_ubicacion"]
    
    if address and "user_zona" in um:
        if address is not None: address += ', ' 
        address += ', ' + um["user_zona"]
    
    um["address"] = address

    return um

filteredUserMetas = filter(filterAddress, userMetas)

# print("Addresses Filtered")
# pp.pprint(filteredUserMetas)

addresses = map(mapAddress, filteredUserMetas)

print("Addresses Parsed")
pp.pprint(addresses)

print("Try to GeoLocate each Address")
adddress_coordinates = geocoding.inject_coordinates_from_google_maps(GOOGLE_MAPS_API_KEY, addresses)

print("adddres_coordinates->")
pp.pprint(adddress_coordinates)


print("Impactar DB")
mssqlconn.insert_coordinates_usermeta(mysql_config, adddress_coordinates)

print("FINISH")