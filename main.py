from time import sleep
from my_API_keys import keys_list
from functions import *

regions = ['eu'] # I only use regions which i have access to
oddsFormat = ['decimal']
markets = ['h2h', 'totals'] # I will only use these two type of bets to make it easier, beacuse they are binary bets (win/lose, over/under), you can find bets explaination in 'utility.md'

i = 16
five_min = 5*60

# after done: while(1):

# get live event odds
while(i in range(0, len(keys_list))):
    response = get_API_response(keys_list[i]) # API call cost = 0
    if(remaning_requests(response) <= 0):
        i += 1  # use next API key
    else:
        response = get_API_response_Odds(keys_list[i], regions[0], markets[1]) # totals odds (over/under), API call cost = 1
        matches_full = response_to_json(response)

        # for each upcoming event, get its bookmakers and their O/U (totals) odds
        upcoming_matches = []
        for match in matches_full:
            totals_odds = []
            for bookmaker in match['bookmakers']:
                bookmaker_totals = bookmaker_totals_odds_shortner(bookmaker)
                totals_odds.append(bookmaker_totals)
            upcoming_matches_element = mathches_totals_odds_shortner(match, totals_odds)
            upcoming_matches.append(upcoming_matches_element)

        a = mathches_short_order_by_points(upcoming_matches)
        print_json_to_file(a, 'upcoming_matches.json')

        i += 1
        sleep(five_min)
        

    
    
