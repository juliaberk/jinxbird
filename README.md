# Jinx Bird

A funny thing happens when a bird watcher wants to add a specific bird to their Life List... it's nowhere to be found!

Jinx Bird is a search tool to help bird watchers spot the specific species that has been ellusive. It is designed to help you in the moment, in the field (assuming you have Wifi or cell service). Jinx Bird will show you on a map where that species was last sighted within a 15 mile radius of your location within the last two weeks. 

## <a name=""></a>Coming Soon:
* Python 3 

## Tech Stack
__Frontend:__  HTML5, Javascript, JQuery, Bootstrap </br>
__Backend:__  Python, Flask, PostgreSQL, SQLAlchemy </br>
__APIs:__ eBird, Wikipedia, Google Maps, Geolocation </br>

## Setup/Installation
#### Requirements:
- PostgreSQL
- Python 2.7
- eBird API key
- Google Maps API key (provided)

To get this app up and running locally, please do the following:

Clone repository:
```
$ git clone https://github.com/juliaberk/jinxbird
```
Create a virtual enviornment:
```
$ virtual env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Sign up at https://ebird.org to get your own API key. Save it to a 'secrets.py' file like so:
```
export ebird_API = 'your key here'
```
