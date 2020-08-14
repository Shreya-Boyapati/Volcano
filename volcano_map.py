import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_range(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

html = """
Volcano name: <br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[41.880784, -87.588455], tiles="Stamen Terrain", zoom_start=4)

fg = folium.FeatureGroup(name="My Map")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fg.add_child(folium.Marker(location=[lt,ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_range(el))))

fg.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(), 
style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000 
else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

legend_html = """
    <div style="position: fixed; 
    bottom: 45px; left: 45px; width: 138px; height: 120px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    ">  <b>Volcanoes of USA</b><br>
    <b><ins>Elevation</ins></b><br>
    <1000      <i class="fa fa-circle" style="color:#008000"></i><br>
    < 3000     <i class="fa fa-circle" style="color:#FFA500"></i><br/>
    >= 3000   <i class="fa fa-circle" style="color:#B22222"></i>
    </div>
"""
map.get_root().html.add_child(folium.Element(legend_html))

pop_legend_html = """
    <div style="position: fixed; 
    bottom: 45px; left: 245px; width: 338px; height: 120px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    ">  <b>World Population</b><br>
    <b><ins>People</ins></b><br>
    <10,000,000      <i class="fa fa-circle" style="color:#90EE90"></i><br>
    10,000,000 - 20,000,000     <i class="fa fa-circle" style="color:#F0E68C"></i><br/>
    20,000,000+   <i class="fa fa-circle" style="color:#F08080"></i>
    </div>
"""
map.get_root().html.add_child(folium.Element(pop_legend_html))



map.add_child(fg)
map.save("Map_html_popup_advanced.html")
