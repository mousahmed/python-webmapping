import folium
import pandas

map = folium.Map(location=[38.5, -99.09], zoom_start=5, tiles="Stamen Terrain")
fg = folium.FeatureGroup(name="My map")
data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


def color_producer(elev):
    if elev <= 1000:
        return "green"
    elif 1000 < elev <= 3000:
        return "orange"
    else:
        return "red"


for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fg.add_child(folium.CircleMarker(
        location=[lt, ln],
        radius=10,
        popup=folium.Popup(iframe),
        fill_color=color_producer(el),
        color="grey",
        fill_opacity=0.7))

fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                      else 'orange' if 20000000 > x['properties']['POP2005'] >= 10000000
                                                      else 'red'}))

map.add_child(fg)
map.save("map1.html")
