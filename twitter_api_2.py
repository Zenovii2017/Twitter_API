from flask import Flask, render_template, request
import folium
from geopy.geocoders import ArcGIS
import twitter_api_1

app = Flask(__name__)


def change_adress(adress):
    """
    (str) -> (list)
    Remake name of position in coordinates
    return list of two coordinates
    """
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(adress)
        Coordinates = [location.latitude, location.longitude]
        return Coordinates
    except:
        return change_adress(adress)


@app.route("/")
def index():
    """
    The function will be return_template
    ("index.html"), the actual form is index.html.
    """
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    """
    it return map with friend or followers
    """
    name = request.input
    map = folium.Map()
    if name == "":
        return render_template("failure.html")
    if request.label["id"] == "Friend":
        TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    else:
        TWITTER_URL = 'https://api.twitter.com/1.1/followers/list.json'
    childs = twitter_api_1.about_user(name, TWITTER_URL)
    for child in childs:
        sentence = ''
        for letters in childs[child]:
            if letters != '`' and letters != "'":
                sentence += letters
        map.add_child(folium.Marker(location=change_adress(child),
                                    popup=sentence,
                                    icon=folium.Icon()))
    map.save(r'/home/zenuk/PycharmProjects/twitter_api/templates/map.html')
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
