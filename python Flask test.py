# //*####

from os import environ, terminal_size


# In your local system project is running on Conda base env
1) open conda terminal
2) go to directory 
    cd C:\Users\chiru\Desktop\running python in vs\DAM
3) run 
    python test.py      e.g its your updated file(in app.py have error  you have changed something)
# python test.py   run comman






# #####













from flask import Flask
from flask import request, jsonify
# pip install earthengine-api
# pip install earthengine-api --upgrade
import ee
import folium
#https://developers.google.com/earth-engine/guides/python_install
#https://developers.google.com/earth-engine/guides/service_account
#https://console.cloud.google.com/apis/library/earthengine.googleapis.com?pli=1&project=manifest-pride-337602

# service_account = "cloud-service...iam.gserviceaccount.com"
# key_path = 'application_default_credentials.json'
# ee.ServiceAccountCredentials('l114422@zeta-instrument-330108.iam.gserviceaccount.com', key_path)

ee.Authenticate()
ee.Initialize()
#cart_classifier = ee.FeatureCollection("users/ee-gupei/randomforest_classifier_3")


app = Flask(__name__)

import json

@app.route("/get_map",  methods=['GET','POST'])
def get_map():
    # if 'cart_classifier' in request.args:
    #     cart_classifier_str = request.args['cart_classifier']
    # else:
    #     title = request.json['cart_classifier']
    #     return "Error: No cart_classifier field provided. Please specify cart_classifier."
    # data1 = request.json
    res = request.data
    json_object = json.loads(res)

    # data = res.json()
    # print(request.data)

    cart_classifier_path = json_object['cart_classifier']
    geometry_path = json_object['geometry']

    # cart_classifier = ee.FeatureCollection("projects/ee-gupei/assets/randomforest_classifier_3")
    # geometry = ee.FeatureCollection("projects/ee-gupei/assets/Final_data_9k")

    cart_classifier = ee.FeatureCollection(cart_classifier_path)
    geometry = ee.FeatureCollection(geometry_path)

    cart_classifier.first()

    # sentinel 2A
    Sentinel2A = ee.ImageCollection("COPERNICUS/S2_SR");
    classifier_string = cart_classifier.first().get('classifier');
    # call ee classifier decisionTree
    classifier = ee.Classifier.decisionTree(classifier_string);

    # set the bands
    BANDS = ['B2', 'B3', 'B4', 'B8'];
    # filter by date range, and Bands
    ic = Sentinel2A.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
    ic = ic.select(BANDS).filterDate('2016-07-01', '2020-12-01').median();
    classified = ic.classify(classifier);
    # input
    a = classified.clip(geometry)
    print(a)
    palette = [
        '0000FF',  # Water
        '008000',  # Veg
        'A52A2A'  # Land
    ]
    lat = -37.8
    lon = 145.2
    Map = folium.Map(locatsion=[lat, lon], zoom_start=10)

    def add_ee_layer(self, ee_image_object, vis_params, name):
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        ).add_to(self)

    folium.Map.add_ee_layer = add_ee_layer

    # Add the image layer to the map and display it.
    # Map.add_ee_layer(classified.clip(geometry), {'palette': palette, 'min': 0, 'max': 2}, 'Classification CART')
    # display(Map)

    return "<p>MAP Return!</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)