from contextlib import nullcontext
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

# f: bookmaker_totals full json -> bookmaker_totals shorter version
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

# f: matches_totals full json -> matches_totals shorter version
def mathches_totals_odds_shortner(match, mathches_totals_odds):
    mathches_totals_odds_short = match
    mathches_totals_odds_short['bookmakers'] = mathches_totals_odds
    return mathches_totals_odds_short

# f: matches_totals shorter version -> version oredred by U/O points

def mathches_short_order_by_points(mathches_totals_odds_short):
    mathches_short_ordered_by_points = []
    for match in mathches_totals_odds_short:
        if(match['bookmakers']): # list is not null
            points = {}
            # get all unique points as keys
            for bookmaker in match['bookmakers']:
                if(bookmaker['totals']['points'] not in points.keys()):
                    points[str(bookmaker['totals']['points'])] = []
            #add element to each corrisponding keys
            for key in points.keys():
                for bookmaker2 in match['bookmakers']:
                    if(str(bookmaker2['totals']['points']) == str(key)):
                        points_elem = {
                            'bookmaker': bookmaker2['bookmaker'],
                            'totals': {
                                'Over': bookmaker2['totals']['Over'],
                                'Under': bookmaker2['totals']['Under']
                            }
                        }
                        points[str(key)].append(points_elem)
            del match['bookmakers']
            match['points'] = points
            mathches_short_ordered_by_points.append(match)
    return mathches_short_ordered_by_points


