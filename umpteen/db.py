
def db():
  '''
  Database reading codes
  '''
  def __init__(self)__:
    return

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
    
    Assumes api_key available in .api_key.txt

    '''
    hidden='👽/.👽'
    # ensure list
    if type(itemNumber) != list:
        itemNumber = [itemNumber]
    try:
        try:  
              api_key = open(hidden).read()
        except:
              print("No API key found for google knowledge")
              print("your installation might be corrupted")
              exit(0)
    except:
        print("failed to read API key from file .api_key.txt")
        print("see: https://console.developers.google.com/apis/credentials?folder=&organizationId=&project=")
        exit(0)

    service_url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query'  : query,
        'limit'  : 10,
        'indent' : True,
        'key'    : api_key
    }

    # get information from url
    url = service_url
    http = urllib3.PoolManager()
    
    try:
        r = http.request('GET', url,fields=params)
        response=json.loads(r.data.decode('utf-8'))
    except:
        print('Error connecting')
        exit(0)
    
    # get items from list
    retval = []
    for value in itemNumber:
        # if we fail on any, we fail on all
        # could make this more tolerant
        try:
            # lets go with the highest score match
            item = response['itemListElement'][value]
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
            retval.append(attributes)
        except:
            retval.append({})
            
    # un-list it if appropriate
    if len(retval) == 1:
        retval = retval[0]
        
    return(retval)