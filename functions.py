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

def print_json_to_file(json_file):
    with open('temp_log.json', 'w') as outfile:
        json.dump(json_file, outfile, indent=4)

