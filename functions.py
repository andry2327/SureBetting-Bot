from requests import get
import json

# HTML API response 

def get_API_response(API_KEY):
    url = 'https://api.the-odds-api.com/v4/sports/?apiKey={}'.format(API_KEY)
    response = get(url)
    return response

def get_API_response_Sports(API_KEY):
    url = 'https://api.the-odds-api.com/v4/sports/?apiKey={}'.format(API_KEY)
    response = get(url)
    return response

def get_API_response_Odds(API_KEY, region, market):
    url = 'https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions={}&markets={}&apiKey={}'.format(
        region, market, API_KEY)
    response = get(url)
    return response

def get_API_response_Scores(API_KEY, sport, days_from):  # set days_from = 0 if you don' need this option
    if(days_from == 0):
        url = 'https://api.the-odds-api.com/v4/sports/{}/scores/?apiKey={}'.format(sport, API_KEY)
    else:
        url = 'https://api.the-odds-api.com/v4/sports/{}/scores/?daysFrom={}&apiKey={}'.format(sport, days_from, API_KEY)
    response = get(url)
    return response


# .json data from html API response

def response_to_json(response):
    response = response.content.decode('utf-8')
    return json.loads(response)


# get API_KEY remaining requests

def remaning_requests(response):
    headers = response.headers
    return int(headers['X-Requests-Remaining'])

# print json to file 'temp_log.json' with indent

def print_json_to_file(json_object):
    with open('temp_log.json', 'w') as outfile:
        json.dump(json_object, outfile, indent=4)

def print_json_to_file(json_object, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(json_object, outfile, indent=4)


# get a shorter json format from the full json upcoming matches api response, for totals odds

# bookmaker_totals full json -> bookmaker_totals shorter version
def bookmaker_totals_odds_shortner(bookmaker_totals):
    bookmaker_key = bookmaker_totals['key']
    totals = {
        'points': float(bookmaker_totals['markets'][0]['outcomes'][0]['point']),
        'Over': float(bookmaker_totals['markets'][0]['outcomes'][0]['price']),
        'Under': float(bookmaker_totals['markets'][0]['outcomes'][1]['price'])
    }
    bookmaker_totals_short = {
        'bookmaker': bookmaker_key,
        'totals': totals
    }
    return bookmaker_totals_short

def mathches_totals_odds_shortner(match, mathches_totals_odds):
    bookmaker_totals_short = match
    bookmaker_totals_short['bookmakers'] = mathches_totals_odds
    return bookmaker_totals_short

