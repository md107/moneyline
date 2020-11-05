import requests
import json

api_key = '0c99967b1d1c94b6e0a2a1fa4e2379db'

sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': api_key})

sports_json = json.loads(sports_response.text)

if not sports_json['success']:
    print('There was a problem with the sports request:', sports_json['msg'])

else:
    print()
    print('Successfully got {} sports'.format(len(sports_json['data'])),'Here\'s the first sport:')
    print(sports_json['data'][0])
    with open('sports.json', 'w') as f:
        json.dump(sports_json['data'], f)

# To get odds for a sepcific sport, use the sport key from the last request
#   or set sport to "upcoming" to see live and upcoming across all sports
sport_key = 'upcoming'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,
    'sport': sport_key,
    'region': 'uk', # uk | us | eu | au
    'mkt': 'h2h' # h2h | spreads | totals
})

odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print('There was a problem with the odds request:',odds_json['msg'])

else:
# odds_json['data'] contains a list of live and 
#   upcoming events and odds for different bookmakers.
# Events are ordered by start time (live events are first)
    print()
    print('Successfully got {} events'.format(len(odds_json['data'])),'Here\'s the first event:')
    print(odds_json['data'][0])
    with open('odds.json', 'w') as f:
        json.dump(odds_json['data'], f)

# Check your usage
    print()
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])


