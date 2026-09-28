import time

from flask import Flask, render_template, request, jsonify, redirect, url_for, Markup
from geopy.geocoders import Nominatim
import censusgeocode as cg

# generated via http://patorjk.com/software/taag/#p=testall&f=Epic&t=RELO%20APP
print(
"""
###################################
#██████╗ ███████╗██╗      ██████╗ #
#██╔══██╗██╔════╝██║     ██╔═══██╗#
#██████╔╝█████╗  ██║     ██║   ██║#
#██╔══██╗██╔══╝  ██║     ██║   ██║#
#██║  ██║███████╗███████╗╚██████╔╝#
#╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ #
###################################
"""
)

import clustervis

app = Flask(__name__)
address = str()

# global to hold most recent results
# specifies defaults if error in address matching
# have a default lat/lon as fallback
MOST_RECENT_RESULTS = {"lat": 40.5218403, "lon": -80.1969462}


def get_coordinates(address):
    """Given a string address, use geolocator api to get address info,
       including lat/lon of searched location.
    """
    try:
        geolocator = Nominatim(user_agent="my_application")
        loc = geolocator.geocode(str(address))
        print(loc.address)
        full_address = loc.address
        latitude = float(loc.latitude)
        longitude = float(loc.longitude)
        return [longitude, latitude], full_address
    except:
        return None


@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/home")
def return_home():
    return render_template("index.html")


@app.route("/search_results", strict_slashes=False, methods=["GET", "POST"])
def search_results():
    # if POST request, update MOST_RECENT_RESULTS, otherwise skip update
    # and re-render page with latest search.
    if request.method == "POST":
        POST_START_TIME = time.time()
        print("search_results called as POST")
        address = request.form["address"]
        MOST_RECENT_RESULTS["address"] = address

        # Get the coordinates (lon/lat) and address for given user search.
        coordinates, full_address = get_coordinates(address)
        print("Currently viewing results for: ", full_address)
        if coordinates:
            print("COORDS FOUND: {}".format(coordinates))
            MOST_RECENT_RESULTS["search_lon"] = coordinates[0]
            MOST_RECENT_RESULTS["search_lat"] = coordinates[1]
        else: # fallback to default example
            pass

        # build visualization object. pass lat/long of searched point.
        cvis = clustervis.ClusterVis(
            lat=MOST_RECENT_RESULTS["search_lat"],
            lon=MOST_RECENT_RESULTS["search_lon"],
        )
        
        # create a map. default view is the top-level, zoomed out map.
        overview = cvis.create_figure()

        # create json from map.
        MOST_RECENT_RESULTS["fig0"] = overview.to_json()

        # Build html tables for display
        t0, t1, t2, t3 = cvis.build_tables()
        MOST_RECENT_RESULTS["t0"] = t0.to_json(orient="index")
        MOST_RECENT_RESULTS["t1"] = t1.to_json(orient="index")
        MOST_RECENT_RESULTS["t2"] = t2.to_json(orient="index")
        MOST_RECENT_RESULTS["t3"] = t3.to_json(orient="index")

        # Attempt to get names of the city, state, and neighborhood
        top_city_names = cvis.get_top_city_names()
        MOST_RECENT_RESULTS["name1"] = top_city_names["t1"]["citystate"]
        MOST_RECENT_RESULTS["name2"] = top_city_names["t2"]["citystate"]
        MOST_RECENT_RESULTS["name3"] = top_city_names["t3"]["citystate"]
        MOST_RECENT_RESULTS["subname1"] = top_city_names["t1"]["neighborhood"]
        MOST_RECENT_RESULTS["subname2"] = top_city_names["t2"]["neighborhood"]
        MOST_RECENT_RESULTS["subname3"] = top_city_names["t3"]["neighborhood"]

        # Get the latitude/longitude of the census tract id'd in the search.
        top_match_coords = cvis.get_top_match_coords()
        MOST_RECENT_RESULTS["c1"] = top_match_coords[0]
        MOST_RECENT_RESULTS["c2"] = top_match_coords[1]
        MOST_RECENT_RESULTS["c3"] = top_match_coords[2]
        
        MOST_RECENT_RESULTS["c1lat"], MOST_RECENT_RESULTS["c1lon"] = [float(x.strip()) for x in top_match_coords[0].split(',')]
        MOST_RECENT_RESULTS["c2lat"], MOST_RECENT_RESULTS["c2lon"] = [float(x.strip()) for x in top_match_coords[1].split(',')]
        MOST_RECENT_RESULTS["c3lat"], MOST_RECENT_RESULTS["c3lon"] = [float(x.strip()) for x in top_match_coords[2].split(',')]

        print('*** Search to render preparation time: {} seconds'.format(round(time.time()-POST_START_TIME, 2)))
        
    return render_template(
        "search_results.html",
        address=MOST_RECENT_RESULTS["address"],
        fig0=MOST_RECENT_RESULTS["fig0"],
        t0=MOST_RECENT_RESULTS["t0"],
        t1=MOST_RECENT_RESULTS["t1"],
        t2=MOST_RECENT_RESULTS["t2"],
        t3=MOST_RECENT_RESULTS["t3"],
        name1=MOST_RECENT_RESULTS["name1"],
        name2=MOST_RECENT_RESULTS["name2"],
        name3=MOST_RECENT_RESULTS["name3"],
        subname1=MOST_RECENT_RESULTS["subname1"],
        subname2=MOST_RECENT_RESULTS["subname2"],
        subname3=MOST_RECENT_RESULTS["subname3"],
        c1=MOST_RECENT_RESULTS["c1"],
        c2=MOST_RECENT_RESULTS["c2"],
        c3=MOST_RECENT_RESULTS["c3"],
        c1lat=MOST_RECENT_RESULTS["c1lat"], c1lon=MOST_RECENT_RESULTS["c1lon"],
        c2lat=MOST_RECENT_RESULTS["c2lat"], c2lon=MOST_RECENT_RESULTS["c2lon"],
        c3lat=MOST_RECENT_RESULTS["c3lat"], c3lon=MOST_RECENT_RESULTS["c3lon"],
    )


@app.route("/about")
def render_about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=False, debug=True)

