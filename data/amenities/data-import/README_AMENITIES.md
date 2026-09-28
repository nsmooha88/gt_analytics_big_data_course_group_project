

# RELO, Amenity Data Download Tool

This script downloads amenities data from the Foursquare Places API and saves the list by state. Once all states' data is downloaded, the same script can be used to merge all the CSVs into a single CSV file.

  
## Pre requisites:

- Client ID and Client Secret from a verified Foursquare Developer account (a "verified" account will have a daily rate limit of 99,500 API calls).

- Ensure the uszips.csv file exists in the same folder as this script

- If running in "merge" mode, ensure that there is no consolidated.csv in the "downloads/<TYPE>" folder already

## Foursquare Developer Account 

### Initial setup

- Go to https://developer.foursquare.com/
- Click on "Create Account" on the top right and fill out the form (name, contact details, etc.)
- Once done, click "Sign Up" at the bottom of the form. 
- Look for the verification email sent to the email provided. 
- Click the verification link in the email body where it is says "Your account is almost set up. Please click ***here*** to verify your email."
- In the login prompt, use the email and password provided in the initial sign up form and log in.
- Now, you should be on the Foursquare Developer Console with the URL on the browser address bar that says https://foursquare.com/developers/apps
- Click on ***Create New App*** in the My Apps section.
- Provide an app name, some URL (http://localhost works) and verify the challenge response activity.
- Click ***Next***.
- Now, you should be on the "App Settings" screen with the CLIENT ID and CLIENT SECRET listed. Copy these 2 IDs so they can be used in the appropriate area in the configuration section of the script.
- Now, you have a Foursquare Developer Sandbox Tier account that has a rate limit of 950 Regular API Calls per day and 50 Premium API Calls per day.

### Verification to increase rate limit

 - The script needs to make many more API calls per hour than provided by the Sandbox Tier.
 - By verifying your account using a credit card, you can upgrade to the Personal Tier to increase this limit to 99,500 Regular API Calls per day and 500 Premium API Calls per day. This does not charge anything.
 - For this, start by clicking on the user icon on the top right on the Developer Console.
 - Click on ***Account*** in the sub menu.
 -  Click on ***Manage Billing*** in the left menu under the ***Account*** menu.
 - Click on the ***Upgrade Now*** button.
 - 3 plans will be displayed. Select the **Personal** plan and click Continue.
 - Provide credit card information and click Submit.

    
## Configurations:

Please set the configuration parameters at the top of the script

- TYPE = An  identifier  for  the  amenity  data  type  being  handled.  Use  anything  you  like.

- CLIENT_ID = Foursquare  Developer  account  client  id  for  Places  API  access

- CLIENT_SECRET = Foursquare  Developer  account  client  secret  for  Places  API  access

- CATEGORY_LIST = Foursquare  venues  categories  that  need  to  be  processed.  Pick  from  https://developer.foursquare.com/docs/build-with-foursquare/categories/

- STATE_LIST = List  of  states  to  pull  data.  Default  list  has  all  states  pre-defined

  

## Usage:

Step 1 
> python process-amenities-data.py import

Step 2 
> python process-amenities-data.py merge

  
## Potential issues:

- API calls may fail and stop the data import. Run step 1 again after removing the state list up to the state that was being processed. Retain the state that failed.
