from requests import get
from pandas import json_normalize


# This method returns the elvation of a locatoin based on lat and long
# https://stackoverflow.com/questions/65748099/open-elevation-api-for-python
def get_elevation(lat = None, long = None):
    '''
        script for returning elevation in m from lat, long
    '''
    if lat is None or long is None: return None
    
    query = ('https://api.open-elevation.com/api/v1/lookup'f'?locations={lat},{long}')
    
    # Request with a timeout for slow responses
    r = get(query, timeout = 20)

    # Only get the json response in case of 200 or 201
    if r.status_code == 200 or r.status_code == 201:
        elevation = json_normalize(r.json(), 'results')['elevation'].values[0]
    else: 
        elevation = None
    return elevation

print(get_elevation(42.3932,72.5277))# elevation of Goessman building