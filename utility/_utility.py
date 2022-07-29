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

upcoming_matches = mathches_short_order_by_points(upcoming_matches)
c = combinations(upcoming_matches[0]["points"]["2.5"], 2)
print_json_to_file(list(c), 'utility/combination.json')

upcoming_matches = mathches_short_order_by_points(upcoming_matches)
print_json_to_file(upcoming_matches, 'utility/upcoming_matches.json')
c = combinations(upcoming_matches[2]["points"]["2.5"], 2)
print_json_to_file(list(c), 'utility/combination.json')
d = C_simple(upcoming_matches[2]["points"]["2.5"], 2)
print_json_to_file(list(d), 'utility/C_simple.json')

upcoming_matches = mathches_short_order_by_points(upcoming_matches)
print_json_to_file(upcoming_matches, 'utility/upcoming_matches.json')
# print(upcoming_matches[i_deb]["points"]["2.5"])
print('N: '+str(len(upcoming_matches[i_deb]["points"]["2.5"]))+'\n')
c = combinations(upcoming_matches[i_deb]["points"]["2.5"], 2)
print_json_to_file(list(c), 'utility/combination.json')
# should be 0.5*N*(N-1)
print('combination.json len: '+str(len(list(c)))+'\n')
d = C_simple(upcoming_matches[i_deb]["points"]["2.5"], 2)
print_json_to_file(list(d), 'utility/C_simple.json')
print('C_simple.json len: '+str(len(list(d)))+'\n')  # should be N*(N-1)

upcoming_matches_comb = get_data_from_json('utility/profittable_matches.json')  # DEBUG
