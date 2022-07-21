from my_API_keys import keys_list
from requests import get
import json

def get_sports(API_KEY):
    url = 'https://api.the-odds-api.com/v4/sports/?apiKey={}'.format(API_KEY)
    sports = get(url)
    sports = sports.content.decode('utf-8')
    return json.loads(sports)
