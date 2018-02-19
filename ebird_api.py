""" This is where the ebird magic happens """

import sys
import requests 
import os
import json

# Check to make sure my ebird token is accessible  
# don't forget to source secrets.sh 
try:
    API_TOKEN = os.environ['ebird_API']

except KeyError:
    print "The key for the ebird API is missing."

#############################################################################


def request_ebird():
    """Send a GET request to ebird using lat, long, species """

    url = "https://ebird.org/ws2.0/data/obs/geo/recent/amecro"

    querystring = {"lat":"37.773972","lng":"-122.431297"}

    headers = {'X-eBirdApiToken': API_TOKEN}

    response = requests.request("GET", url, headers=headers, params=querystring)

    ebird_json = response.json()

    print ebird_json


request_ebird()