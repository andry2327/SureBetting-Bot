from time import sleep
from datetime import datetime
from API_keys import keys_list, token
from pathlib import Path
if Path('_API_keys.py').exists():
   from _API_keys import keys_list, token
from functions import *
import logging

import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

bot = telepot.Bot(token)
bot.message_loop(handle)

regions = ['eu'] # I only use regions which i_key have access to
oddsFormat = ['decimal']
markets = ['h2h', 'totals'] # I will only use these two type of bets to make it easier, beacuse they are binary bets (win/lose, over/under), you can find bets explaination in 'utility.md'

profittable_matches_bet_list = []
curr_day = str(datetime.now().strftime("%d"))

i_key = 0
five_min = 5*60
ten_min = 10*60
profittable_matches_count = 0
API_response_fetch = 0
EURO_STARTING_BALANCE = 10000  
PROFIT_PERCENTAGE_UPPER_LIMIT = 0.2 # only matches with al least 2% profit will be shown on output
EURO_STARTING_BALANCE = input('Insert your starting balance in € (-1 to start with 10000€): ')

if(float(EURO_STARTING_BALANCE) == -1):
    EURO_STARTING_BALANCE = 10000

BALANCE_AMOUNT_RATIO = 0.1  # for each bet, the stake will be 1/10 of current balance

EURO_BALANCE = float(EURO_STARTING_BALANCE)

#reset log file
with open('exec.log', 'w'):
    pass

logging.basicConfig(filename="exec.log",
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("START .py script\n\n")

# remove empty str in keys_list
keys_list = list(filter(None, keys_list))

while(1):
    # get live event odds
    while(i_key in range(0, len(keys_list))):
        if(str(datetime.now().strftime("%d")) != curr_day):
            curr_day = str(datetime.now().strftime("%d"))
            # it updates the balance every new day, adding previous day bet returns
            for gain in list(map(lambda x: x['EURO_back'], profittable_matches_bet_list)):
                EURO_BALANCE += gain
            send_message(bot, chat_id, 'BALANCE UPDATE -> current balance: ' +
                         str(round(EURO_BALANCE, 2)) + '€')
            sleep(10)
            profittable_matches_bet_list.clear() # list reset every day
        response = get_API_response(keys_list[i_key])  # API call cost = 0
        if(remaning_requests(response) <= 0):
            i_key += 1  # use next API key
        else:
            # totals odds (over/under), API call cost = 1
            response = get_API_response_Odds(keys_list[i_key], regions[0], markets[1])
            API_response_fetch += 1
            matches_full = response_to_json(response)
            logger.info('START API fetch N: ' + str(API_response_fetch))
            # for each upcoming event, get its bookmakers and their O/U (totals) odds
            upcoming_matches = []
            for match in matches_full:
                totals_odds = []
                for bookmaker in match['bookmakers']:
                    bookmaker_totals = bookmaker_totals_odds_shortner(bookmaker)
                    totals_odds.append(bookmaker_totals)
                upcoming_matches_element = mathches_totals_odds_shortner(match, totals_odds)
                upcoming_matches.append(upcoming_matches_element)
            upcoming_matches = mathches_short_order_by_points(upcoming_matches)

            # for each upcoming match, for each totals (U/O) points, create bookmakers couples
            upcoming_matches_comb = []
            for upcoming_match_elem in upcoming_matches:
                upcoming_matches_points = {}
                for points_key, points in upcoming_match_elem['points'].items():   
                    upcoming_matches_points_elem = [] 
                    if (len(points) > 1):  # I can only create bookmakers couples if there are 2 ore more
                        points_elem = C_simple(points, 2)
                        upcoming_matches_points[str(points_key)] = points_elem
                upcoming_matches_comb_elem = upcoming_match_elem
                upcoming_matches_comb_elem['points'] = upcoming_matches_points
                upcoming_matches_comb.append(upcoming_matches_comb_elem)

            # get profittable matches
            match_index = 0
            bet_info = {}
            for match in upcoming_matches_comb:
                if (match['points']):
                    for points_key, points in match['points'].items():
                        for points_elem in points:
                            bet_info['key'] = bet_id_format(
                                match['id'], points_key, points_elem['bookmaker_1'], points_elem['totals']['Over_1'], points_elem['bookmaker_2'], points_elem['totals']['Under_2'])
                            if(is_bookmakers_combinations_profitable(points_elem) and (bet_info['key'] not in list(map(lambda x: x['key'], profittable_matches_bet_list)))):
                                bet_profit_percentage = get_profits_percentage(points_elem['totals']['Over_1'], points_elem['totals']['Under_2'])
                                if(bet_profit_percentage > PROFIT_PERCENTAGE_UPPER_LIMIT):
                                    bet_info['perc'] = bet_profit_percentage
                                    # win, bet amount and info
                                    WIN_AMOUNT = EURO_BALANCE*BALANCE_AMOUNT_RATIO
                                    stake_A = get_stake_from_quote(points_elem['totals']['Over_1'], WIN_AMOUNT)
                                    stake_B = get_stake_from_quote(points_elem['totals']['Under_2'], WIN_AMOUNT)
                                    EURO_BALANCE -= stake_A + stake_B
                                    text_match = create_text(match, points_key, points_elem, stake_A, stake_B, WIN_AMOUNT)
                                    write_to_file_profittable_matches(text_match)
                                    profittable_matches_count += 1

                                    profit = WIN_AMOUNT - (stake_A + stake_B)
                                    sum_A_B_profit = stake_A + stake_B + profit
                                    bet_info['EURO_back'] = sum_A_B_profit

                                    profittable_matches_bet_list.append( bet_info)
                                
                                    # file update
                                    logger.info('MATCH FOUND: ' + '\n\n' + text_match)
                                    logger.info('FOUND MATCHES AMOUNT: ' + str(profittable_matches_count))

                                    # telegram message
                                    send_message(bot, chat_id, text_match)
                                    sleep(10)
                                    send_message(bot, chat_id, 'current balance: ' + str(round(EURO_BALANCE, 2)) + '€')
                                    sleep(30)
                            else:
                                logger.info('fetch N ' + str(API_response_fetch) +
                                            ', MATCH ' + str(match_index) + ': NO FOUND')
                match_index += 1
            logger.info('END API fetch N: ' + str(API_response_fetch) + ', balance: ' + str(round(EURO_BALANCE, 2)) + '€')
            i_key += 1
            sleep(five_min)
    i_key = 0
