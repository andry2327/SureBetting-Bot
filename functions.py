from requests import get
import json

def get_sports(API_KEY):
    url = 'https://api.the-odds-api.com/v4/sports/?apiKey={}'.format(API_KEY)
    sports = get(url)
    sports = sports.content.decode('utf-8')
    return json.loads(sports)

def get_odds(API_KEY, region, market):
    url = 'https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions={}&markets={}&apiKey={}'.format(region, market, API_KEY)
    odds = get(url)
    odds = odds.content.decode('utf-8')
    return json.loads(odds)

def get_scores(API_KEY, sport, days_from):  # set days_from = 0 if you don' need this option
    if(days_from==0):
        url = 'https://api.the-odds-api.com/v4/sports/YOUR_SPORT_KEY/scores/?apiKey=YOUR_API_KEY'.format(sport, API_KEY)
    else:
        url = 'https://api.the-odds-api.com/v4/sports/YOUR_SPORT_KEY/scores/?daysFrom=YOUR_DAYS_FROM&apiKey=YOUR_API_KEY'.format(sport, days_from, API_KEY)

    scores = get(url)
    scores = scores.content.decode('utf-8')
    return json.loads(scores)
