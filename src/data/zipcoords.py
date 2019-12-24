from uszipcode import SearchEngine

def zipcode_to_coords(zipcode):
    search = SearchEngine(simple_zipcode=True)
    zip_obj = search.by_zipcode(str(zipcode)[0:6])
    zip_dct = zip_obj.to_dict()
    lat = zip_dct['lat']
    lng = zip_dct['lng']
    return lat, lng

if __name__ == '__main__':
    print(zipcode_to_coords(59601))