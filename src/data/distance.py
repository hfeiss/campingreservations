from uszipcode import SearchEngine
import geopy.distance as dist

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


def get_dst(lat_one, lng_one, lat_two, lng_two):
    coords_one = (lat_one, lng_one)
    coords_two = (lat_two, lng_two)
    return dist.distance(coords_one, coords_two).miles


if __name__ == '__main__':
    helena = zipcode_to_coords('59601-0112')
    portland = zipcode_to_coords(97211)
    print(f'Helena is at {helena}')
    print(f'Porltand is at {portland}')
    distance = get_dst(helena[0], helena[1],
                       portland[0], portland[1])
    print(f'The distance between the two is {distance:.2f} miles')
