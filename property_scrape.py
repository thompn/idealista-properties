import base64, os, json, requests
import pandas as pd
from pandas.io.json import json_normalize

# function to get oauth token for use in search request

def get_auth():
    apikey = 'api key' # replace with idealista api key
    secret = 'api secret key' # replace with idealisa secret key
    # encode the key in the correct format to base64
    basekey = base64.b64encode(bytes(apikey +':'+ secret, 'utf-8'))
    key = 'Basic ' + basekey.decode()
    # set oauth request url
    url = "http://api.idealista.com/oauth/token"
    grant_type = 'client_credentials'
    # set headers for request
    headers = {'Authorization': key, 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    # set payload for request
    data = {'grant_type' : grant_type}
    # send POST request to server for oAuth key
    r = requests.post(url, data, headers=headers)
    c = r.content
    # pass the request response to json object
    json_obj = json.loads(c.decode())
    return json_obj

# function to POST request to api to return properties
def do_search(token):
    # example search url, see api docs for options
    url = "http://api.idealista.com/3.5/es/search?center=41.386347,2.169283&operation=rent&propertyType=homes&country=es&maxItems=10&distance=1000"
    # set headers to contain token for POST request
    headers = {'Authorization' : 'Bearer ' + token}
    response = requests.post(url,headers=headers)
    # return the response from api, returned as JSON
    return response

# parse through request and assign each object to a var
json_obj = get_auth(key)
token = json_obj['access_token']
ttype = json_obj['token_type']
expires_in = json_obj['expires_in']
scope = json_obj['scope']
jti = json_obj['jti']

# POST request using returned token
# and return to var 'results'
results = do_search(token)

# store as json object
results = results.json()

# send json to dataframe using elementList as key
pdf = pd.DataFrame(results['elementList'])
