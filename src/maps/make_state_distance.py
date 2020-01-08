import pandas as pd
import folium
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
cleanpath = os.path.join(datapath, 'cleaned/')
imagepath = os.path.join(rootpath, 'images/')

states = pd.read_csv('states.csv')
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'

def make_maps(sourcepath, years=None):
    list_years = []
    if years:
        list_years = years
    else:
        for root, dirs, file in os.walk(sourcepath):
            list_years.extend(file)
    list_years.sort()

    for year in list_years:
        distance = pd.read_pickle(sourcepath + year)
        print(f'Wrote {str(year[:-4])}')

        distance = distance[distance['CustomerState'].isin(states['States'])]
        distance.reset_index(inplace = True, drop = True)
        distance.sort_values('CustomerState', inplace = True)

        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            name='choropleth',
            data=distance,
            columns=['CustomerState', 'avg(DistanceTraveled)'],
            key_on='feature.id',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Distance Traveled (miles)'
        ).add_to(m)

        folium.LayerControl().add_to(m)

        m.save(f'{imagepath}maphtmls/{str(year[:-4])}.html')

if __name__ == '__main__':
    
    make_maps(cleanpath + 'DistanceByCustomerState/')