import folium
import pandas as pd

map = folium.Map(location=[45,-99], zoom_start=6, tiles="Mapbox bright")

pointData = pd.read_csv("Volcanoes.txt")
lat = list(pointData["LAT"])
lon = list(pointData["LON"])
elev = list(pointData["ELEV"])

def colourPoint(height):
	if height < 1000:
		return "green"
	elif 1001<height<2000:
		return "orange"
	else:
		return "red"


fg = folium.FeatureGroup(name="My Map")

for lt,ln,el in zip(lat,lon,elev):
	fg.add_child(folium.CircleMarker(location=[lt,ln], popup=str(el), icon = folium.Icon(color=colourPoint(el))))

map.add_child(fg)
map.save("NewMap.html")

