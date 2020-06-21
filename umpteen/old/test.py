import urllib3
import json
import sys
import wikipedia

from db import Db

ddb = Db()
itemNumber = 0

query = '7 Eleven®'

# ensure list
if type(itemNumber) != list:
    itemNumber = [itemNumber]

#https://www.mediawiki.org/wiki/API:Tutorial
url = wikipedia.API_URL
params = {
        'action'   : 'query',
        'limit' : 1,
        'list': 'search',
        'srsearch' : query,
        'namespace' : 0,
         'format' : 'json'
    }

params = {
        'action'   : 'opensearch',
        'limit' : 1,
        'search' : query,
        'namespace' : 0,
         'format' : 'json'
    }

retval = []
try:
  response = ddb.get(url,params)[-1]
  print(response)
  for value in itemNumber:
    # if we fail on any, we fail on all
    # could make this more tolerant
    try:
      item = response['search'][value]

      pageid = item['pageid']

      attributes = {
        'name'   :  item['title'],
        'blurb'  :  item['snippet'],
        'wikipedia pageid' :  item['pageid']
      }


      retval.append(attributes)
    except:
      retval.append({})
except:
  pass

# un-list it if appropriate
if len(retval) == 1:
    retval = retval[0]

print(retval)
