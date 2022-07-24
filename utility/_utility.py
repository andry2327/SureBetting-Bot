# get json API response

from requests import get
import json
from main import *
from functions import *

url = "https://api.wheretheiss.at/v1/satellites/25544"
response = get(url)

# dump response into json
result = response.content.decode('utf-8')
result = json.loads(result)
print(result)  # print raw json

# print as key-value pairs
for item in result:
    print("{0} : {1}".format(item, result[item]))

# for debugging
print_json_to_file(upcoming_matches, 'totals_odds.json')
a = mathches_short_order_by_points(upcoming_matches)
print_json_to_file(a, 'totals_odds_ordered.json')
