import csv
import time
import http.client
import json
import os
import sys


CATEGORY_LIST =["4bf58dd8d48988d112951735"] #Reference : https://developer.foursquare.com/docs/build-with-foursquare/categories/
TYPE = "ENTER AMENITY TYPE (ex:hardware)"
CLIENT_ID = "ENTER CLIENT ID"
CLIENT_SECRET = "ENTER CLIENT SECRET"
STATE_LIST = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

zip_code_file_path = "uszips.csv" # Reference : https://simplemaps.com/data/us-zips
venue_list = []
  
# Loops through the states and calls the functions to download location data.
def importData():     

    for s in STATE_LIST:
        venue_list.clear()
        zips_csv = csv.reader(open(zip_code_file_path))
        zips_csv = list(zips_csv)[1:]
        zips = [(n[0], n[3], n[4]) for n in zips_csv]

        for zip in zips:
            if zip[2] in [s]:
            #if zip[0] in ["46001"]:
                #print(zip[0] + zip[1] + zip[2])
                getVenues(zip[0], zip[1], zip[2])
        printCsv(s)

# Calls the Foursquare API to get the venues for the zip provided.
def getVenues(zip: str, city:str, state:str):
    
    time.sleep(0.8) # Sleep added to support the 5000 calls per hour API rate limit in a continuous run
    print("Calling zip - " + zip + " of " + city + " "+ state)
    print("Loading "+TYPE+" data") 

    category_string = ""
    for category in CATEGORY_LIST:
        category_string = category_string + category + ","
    category_string = category_string[0:-1]

    print("Pulling categories - "+category_string)

    # Calling Foursquare places API to retrieve venue list in the given zip matching the category list.
    conn = http.client.HTTPSConnection("api.foursquare.com")
    conn.request("GET", "/v2/venues/search?intent=browse&categoryId="+category_string+"&client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&v=20200604&near="+zip)
    response = conn.getresponse()
    venueList = response.read()

    jsonResponse = json.loads(venueList)

    # Process the response to extract venue data relevant for RELO.
    if ("venues" in jsonResponse["response"]):    
        for venue in jsonResponse["response"]["venues"]:
            if (venue["categories"][0]["id"] in CATEGORY_LIST): #Sometimes different category types get returned by the API. Handling those here.
                temp = {
                    "zip" : zip,
                    "city": city,
                    "state": state,
                    "name":venue["name"],
                    "address": (venue["location"]["address"] if ('address' in venue["location"]) else "not_available"),
                    "postalCode": (venue["location"]["postalCode"] if ('postalCode' in venue["location"]) else "not_available"),
                    "lat":venue["location"]["lat"],
                    "lon":venue["location"]["lng"]
                }            
                
                # Ensuring that only unique addresses get persisted.
                if not any((x["address"] == temp["address"] and x["postalCode"] == temp["postalCode"]) for x in venue_list):
                    venue_list.append(temp)
                   
    else:
        print("No venues. Skipping +"+zip)


# Persists csv file with venue data for a state.
def printCsv(state:str):
    if not os.path.exists("downloads/"+TYPE):
        os.makedirs("downloads/"+TYPE)

    with open("downloads/"+TYPE+"/out-"+TYPE+"-"+state+".csv", "w", newline='',encoding="utf-8") as f:
        wr = csv.DictWriter(f, delimiter=",",fieldnames=list(venue_list[0].keys()), dialect='excel',quoting=csv.QUOTE_NONNUMERIC)
        wr.writeheader()
        wr.writerows(venue_list)

# Merges state level venue data csvs in to a consolidatest csv file.
def mergeCSVs():
    csv_header = "\"zip\",\"city\",\"state\",\"name\",\"address\",\"postalCode\",\"lat\",\"lon\""
    root_dir = "downloads/"+TYPE
    csv_out = root_dir+"/consolidated.csv"

    csv_dir = root_dir

    dir_tree = os.walk(csv_dir)
    for dirpath, dirnames,filenames in dir_tree:
        pass

    csv_list = []
    for file in filenames:
        if file.endswith('.csv'):
            csv_list.append(file)

    print(csv_list)

    csv_merge = open(csv_out, 'w',encoding="utf-8")
    csv_merge.write(csv_header)
    csv_merge.write('\n')

    for file in csv_list:
        csv_in = open(root_dir+"/"+file,encoding="utf-8")
        for line in csv_in:
            if line.startswith(csv_header):
                continue
            csv_merge.write(line)
        csv_in.close()
    
    csv_merge.close()

#Prints usage instructions
def printUsage():
    print("\n*********************************************************************************************\n")
    print("\nRELO amenity data download tool")
    print("----------------------------------")
    print("This script downloads amenities data from the Foursquare Places API and saves the list by state. Once all states' data is downloaded, the same script can be used to merge all the CSVs to a single CSV file.\n")
    print("Pre requisites:")
    print("- Client ID and Client Secret from a verified Foursquare Developer account (a 'verified' accrount will have a daily rate limit of 99,500 API calls).")
    print("- Ensure the uszips.csv file exists in the same folder as this script")
    print("- If running in 'merge' mode, ensure that there is no consolidated.csv in the 'downloads/<TYPE>' folder already")
    print("\nConfigurations:")
    print("Please set the configuration parameters at the top of the script")
    print("- TYPE = <An identifier for the amenity data type being handled. Use anything you like.>")
    print("- CLIENT_ID = <Foursquare Developer account client id for Places API access>")
    print("- CLIENT_SECRET = <Foursquare Developer account client secret for Places API access>")
    print("- CATEGORY_LIST = <Foursquare venues categories that need to be processed. Pick from https://developer.foursquare.com/docs/build-with-foursquare/categories/>")
    print("- STATE_LIST = <List of states to pull data. Default list has all states pre-defined>")
    print("\nUsage:")
    print("Step 1 >> python process-amenities-data.py import")
    print("Step 2 >> python process-amenities-data.py merge")
    print("\nPotential issues:")
    print("- API calls may fail and stop the data import. Run step 1 again after removing the state list up to the state that was being processed. Retain the state that failed.")
    print("\n**********************************************************************************************\n")
  

if __name__=="__main__": 
    if(len(sys.argv) < 2):
        printUsage()
        sys.exit()
    if(sys.argv[1]=='import'):
        importData()
    elif(sys.argv[1] =='merge'):
        mergeCSVs()
    else:
        print("Incorrect arguments!")
        printUsage()
