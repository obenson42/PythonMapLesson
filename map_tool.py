import branca
import folium
import pandas

# elevations between about 750 and 4300 => 0 and 4
def color_from_elevation(el):
    colors = ['black', 'darkred', 'red', 'lightred', 'white']
    indx = (4 * el) // 4300
    if indx < 0:
        indx = 0 
    if indx > 4:
        indx = 4 
    return colors[int(indx)]

# populations between about 1000000 and 1000000000 => 0 and 4
def color_from_population(pop):
    colors = ['black', 'darkred', 'red', 'lightred', 'white']
    indx = (4 * pop) // 100000000
    if indx < 0:
        indx = 0 
    if indx > 4:
        indx = 4 
    return colors[int(indx)]

map = folium.Map(location=[38.58, -110], zoom_start=6, tiles="Stamen Terrain")

volcanoes = pandas.read_csv("volcanoes.txt")

fgv = folium.FeatureGroup(name="Volcanoes")

lat = list(volcanoes["LAT"])
lon = list(volcanoes["LON"])
names = list(volcanoes["NAME"])
status = list(volcanoes["STATUS"])
type = list(volcanoes["TYPE"])
elev = list(volcanoes["ELEV"])

cssLink = "<link rel='stylesheet' href='map.css'/>"

html = """<div class='volcano_info'>
<a href='https://www.google.co.uk/search?q=volcano %s' target='_blank'>%s</a>
</div>
<span class='info_label'>Height:</span> %sm<br>
<span class='info_label'>Status:</span> %s"""

for lt, ln, nm, st, ty, el in zip(lat, lon, names, status, type, elev):
    iframe = branca.element.IFrame(html=html % (nm, nm, str(el), st), width=300, height=100)
    color = color_from_elevation(el)
    if st == 'Historical':
        fgv.add_child(folium.Marker(location=[lt, ln], popup=cssLink + html % (nm, nm, str(el), st), icon=folium.Icon(color=color, icon_color='gray')))
    else:
        fgv.add_child(folium.CircleMarker(location=[lt, ln], color=color, fill_color=color, fill=True, popup=cssLink + html % (nm, nm, str(el), st)))

fgp = folium.FeatureGroup(name="Countries")
fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding="utf-8-sig").read(), style_function=lambda x: {'fillColor':color_from_population(x["properties"]["POP2005"])}))

map.add_child(fgp) # add country population first otherwise user can't click on volcanoes for info
map.add_child(fgv)

map.add_child(folium.LayerControl())

map.save("Map1.html")
