import umpteen


db = umpteen.Db()

test = 'Google Knowledge test'
#-----------------------------
inputs = ['W Hotels®']
output = [{'name': 'W Hotels', 'type': ['Brand', 'Place', 'Thing'], 'blurb': 'W Hotels is an upscale hotel chain owned by Marriott International that is generally marketed towards a younger age group than their other properties. ', 'url': 'https://en.wikipedia.org/wiki/W_Hotels', 'image': 'https://commons.wikimedia.org/wiki/File:W_Hotels_Logo.svg', 'description': 'Hotel chain'}]
deleter = 'resultScore'

for i,inp in enumerate(inputs):
  tester = db.GoogleKnowledge(inp)
  del tester[deleter]
  try:
    assert tester.items() == output[i].items()
  except AssertionError:
    print(test)
    print('AssertionError',i,inp)
    print(tester)
    print(output[i])
