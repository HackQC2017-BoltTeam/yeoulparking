import csv
import os

from math import asin
from math import cos
from math import radians
from math import sin
from math import sqrt

from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)


def convert_to_float(number_string):
    """Convert comma-delimited real numberts in string format to a float
    >>> convert_to_float("-79,1")
    -79.1
    """
    return(float(number_string.replace(',', '.')))


def normalize_attribute(key):
    return key.replace(' ', '_').lower()


def normalize_attributes(row):
    return {normalize_attribute(key): value for key, value in row.items()}


def get_parking_id(id_string):
    """Get parking ID as an integer if any, otherwise None"""
    if id_string:
        return int(id_string)
    else:
        return None


# All non-string values will be converted with these functions
TYPE_CONVERSIONS = {
    'id_sta': get_parking_id,
    'nbr_place': int,
    'latitude': convert_to_float,
    'longitude': convert_to_float,
}


def convert_row(row):
    for attribute, convert_function in TYPE_CONVERSIONS.items():
        row[attribute] = convert_function(row[attribute])
    return row


def read_parking_data():
    results = []
    with open("data/infoneigelistedesstationnementsgratuits20152016.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ",", quotechar = '"')
        for row in reader:
            row = normalize_attributes(row)
            results.append(convert_row(row))
    return results


PARKINGS = read_parking_data()


class Location:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_distance(self, latitude, longitude):
        """Return the distance from another latitude/longitude"""
        return self.compute_haversine_distance(self.latitude, self.longitude,
                                               latitude, longitude)

    @staticmethod
    def compute_haversine_distance(lat1, long1, lat2, long2):
        """Compute the distance between two lat/long pairs"""
        long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2])
        delta_long = long2 - long1
        delta_lat = lat2 - lat1
        hav = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2
        return 2 * asin(sqrt(hav)) * 6367


def get_parkings_by_distance(location):
    results = PARKINGS.copy()
    for result in results:
        result['distance'] = location.get_distance(result['latitude'], result['longitude'])
    return sorted(results, key=lambda result: result['distance'])


@app.route("/ping")
def ping():
    return "pong"


@app.route('/parkings')
def get_parkings():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if latitude is not None and longitude is not None:
        latitude = convert_to_float(latitude)
        longitude = convert_to_float(longitude)
        location = Location(latitude, longitude)
        results = get_parkings_by_distance(location)
    else:
        results = PARKINGS
    return jsonify({'data': results})


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)
