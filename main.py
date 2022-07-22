from time import sleep
from my_API_keys import keys_list
from functions import *

regions = ['eu'] # I only use regions which i have access to
oddsFormat = ['decimal']
markets = ['h2h', 'totals'] # I will only use these two type of bets to make it easier, beacuse they are binary bets (win/lose, over/under), you can find bets explaination in 'utility.md'

i = 0
five_min = 5*60

# after done: while(1):

# get live event odds
while(i in range(0, len(keys_list))):
    response = get_API_response(keys_list[i]) # API call cost = 0
    if(remaning_requests(response) <= 0):
        i += 1  # use next API key
    else:
        response = get_API_response_Odds(keys_list[i], regions[0], markets[1]) # totals odds (over/under), API call cost = 1
        live_matches_full = response_to_json(response)
        i += 1
        sleep(five_min)
        

    
    
