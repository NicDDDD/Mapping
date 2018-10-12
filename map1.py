import folium
import pandas as pd
import json

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

geo_json_data = json.load(open("world.json", "r", encoding = "utf-8-sig"))

def findMin(dictData):
	minVal  = 30000000000
	for i in range(len(dictData["features"])):
		if dictData["features"][i]["properties"]["POP2005"] < minVal:
			minVal = dictData["features"][i]["properties"]["POP2005"]
	return minVal

def findMax(dictData):
	maxVal  = 0
	for i in range(len(dictData["features"])):
		if dictData["features"][i]["properties"]["POP2005"] > maxVal:
			maxVal = dictData["features"][i]["properties"]["POP2005"]
	return maxVal

linear = folium.LinearColormap(["green","yellow","orange","red"], index=[findMax(geo_json_data)/20,findMax(geo_json_data)/15,findMax(geo_json_data)/10,findMax(geo_json_data)], vmin=findMin(geo_json_data), vmax=findMax(geo_json_data))

fgv = folium.FeatureGroup(name="Volcanoes")

for lt,ln,el in zip(lat,lon,elev):
	fgv.add_child(folium.CircleMarker(location=[lt,ln], radius = 6,popup=str(el)+" m", fill_color=colourPoint(el), color="grey", fill_opacity=0.7))


fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(geo_json_data, style_function = lambda feature: {"fillColor" : linear(feature["properties"]["POP2005"])} ))



map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())
map.save("NewMap.html")


