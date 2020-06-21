import urllib3
import json
import sys
import wikipediaapi

class Db:
  '''
  Database reading codes
  '''
  def __init__(self,lang='en'):
    self.error = []
    self.lang = lang
    self.wiki_wiki = wikipediaapi.Wikipedia(self.lang)

  def run(self,query='Taylor Swift'):
    '''
    Run through all databases defined
    setting up attributes
    '''
    self.attributes = self.GoogleKnowledge(query=query)


  def get(self,url,params):
    '''
    get information from url
    with parameters params

    Note: uses urllib3 and assumes json response
    '''

    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url,fields=params)
        response=json.loads(r.data.decode('utf-8'))
    except:
        self.error.append(['Error in get() call:',url,params])
        return(None)

    return(response)
 
  def Wikipedia(self,query='Taylor Swift',itemNumber=0):
    '''
    Pull some information on a topic (person, company etc)
    described in `query` (e.g. 'Mickey Mouse')

    return:         Dictionary of attributes of entry in
                    Wikipedia

    '''
    page_py = self.wiki_wiki.page(query)


    attributes = {
        'name'       : page_py.title,
        'blurb'      : page_py.summary
    }

    return(attributes)

    
 
  def GoogleKnowledge(self,query='Taylor Swift',itemNumber=0):
    '''
    Pull some information on a topic (person, company etc)
    described in `query` (e.g. 'Mickey Mouse')
    
    itemNumber(s) : which item(s) to select (by score)
                    default is 0 (1st item: highest score)
                    This will generally be fine, but may fail
                    with something obscure and you need to use a diifferent 
                    itemNumber. It can be a list, in which case the 
                    return is a list of dictionaries.

                 
    return:         Dictionary of attributes of entry in 
                    Google knowledge graph. This will be a list if
                    itemNumber is a list
    
    Assumes api_key available

    Details of API on:
    https://developers.google.com/knowledge-graph

    Attributes are:

    service_url = "https://kgsearch.googleapis.com/v1/entities:search"
    item=response['itemListElement'][value]
    attributes = {
        'name'       : item['result']['name'],
        'type'       : item['result']['@type'],
        'blurb'      : item['result']['detailedDescription']['articleBody'],
        'url'        : item['result']['detailedDescription']['url'],
        'image'      : item['result']['image']['url'],
        'resultScore': item['resultScore'],
        'description': item['result']['description']
    }


    '''

    self.GoogleKnowledgeAPI='👽/.👽'
    try:
        api_key = open(self.GoogleKnowledgeAPI).read().strip()
    except:
        print("failed to read API key")
        print("see: https://console.developers.google.com/apis/credentials?folder=&organizationId=&project=")
        sys.exit(0)

    url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query'  : query,
        'limit'  : 1,
        'indent' : True,
        'key'    : api_key
    }


    try:
        response = self.get(url,params)['itemListElement']
    except:
        return({})

    item = response[0]
    # if we fail on any, we fail on all
    # could make this more tolerant
    try:
        # pull some attributes and put them in 
        # a dictionary called attributes
        attributes = {
        'name'       : item['result']['name'],
        'type'       : item['result']['@type'],
        'blurb'      : item['result']['detailedDescription']['articleBody'],
        'url'        : item['result']['detailedDescription']['url'],
        'image'      : item['result']['image']['url'],
        'resultScore': item['resultScore'],
        'description': item['result']['description']
        }
        return(attributes)
    except:
        # error code this
        pass       

    return {}


if __name__ == "__main__":
  db = Db()
  resp = db.GoogleKnowledge("hello world")
  print(resp)

  resp = db.Wikipedia("hello world")
  print(resp)

