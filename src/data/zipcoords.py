from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)

def zipcode_to_coords(zipcode):
    zip_obj = search.by_zipcode(str(zipcode)[0:5])
    zip_dct = zip_obj.to_dict()
    lat = zip_dct['lat']
    lng = zip_dct['lng']
    return lat, lng

def get_lat(zipcode):
    zip_obj = search.by_zipcode(str(zipcode)[0:5])
    zip_dct = zip_obj.to_dict()
    return zip_dct['lat']
 

def get_lng(zipcode):
    string = str(zipcode)
    zip_obj = search.by_zipcode(string[0:5])
    zip_dct = zip_obj.to_dict()
    return zip_dct['lng']
   

if __name__ == '__main__':
    print(zipcode_to_coords(59601))