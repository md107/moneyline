import json

f = open('odds.json')
odds = json.load(f)

for odd in odds:
    team1, team2 = odd['teams']
    odds = []
    for site in odd['sites']:
        odds.append(site['odds']['h2h'])
    print(odds)
