import pandas as pd
import folium
import os
import time
import selenium.webdriver
import branca

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

        m = folium.Map(location=[48, -102], tiles='cartodbpositron', zoom_start=3)
        #m = folium.Map(location=[48, -102], tiles='Mapbox Bright', zoom_start=2.5)
        colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 50e3)


        folium.Choropleth(
            geo_data=state_geo,
            name='choropleth',
            data=distance,
            columns=['CustomerState', 'avg(DistanceTraveled)'],
            key_on='feature.id',
            fill_color='GnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            nan_fill_opacity=0.0,
            bins=[x for x in range(0, 4000, 500)],
            legend_name=f'{year[:-4]} (distance in miles)'
        ).add_to(m)

        folium.LayerControl().add_to(m)

        m.save(f'maphtmls/CustomerState/{str(year[:-4])}.html')

def make_images():
    list_years = []
    for root, dirs, file in os.walk('./maphtmls'):
        list_years.extend(file)
    list_years.sort()    
    delay = 5
    for year in list_years:
        tmpurl = f'file://{srcpath}/maps/maphtmls/CustomerState/{year}'
        print(tmpurl)
        browser = selenium.webdriver.Safari()
        browser.get(tmpurl)
        time.sleep(delay)
        browser.save_screenshot(f'{imagepath}/maps/CustomerState/{str(year[:-5])}.png')
        browser.quit()


if __name__ == '__main__':

    make_maps(cleanpath + 'DistanceByCustomerState/')
    make_images()
