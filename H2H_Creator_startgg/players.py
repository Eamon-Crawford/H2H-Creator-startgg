# File for getting all player info from the list of players provided

import json
from .api import run_query
from .queries import PLAYERS_QUERY
from time import sleep
from .exceptions import *

def get_players_info(players:list, save_json:bool, header, sleep_time):
    players_info = {}

    i = 0
    a = False
    while (i < len(players)):
        variables = {"slug": players[i]}
        response = run_query(PLAYERS_QUERY, variables, header) # Get response from server
        if response == 500 or response == 429 or response == 404 or response == 400: # If server error
            print("Error code {} Retrying player {} in 10 seconds, slug {}".format(response, i, players[i]))
            sleep(10)
        else:
            if response['data']['user'] is None:
                i += 1
                continue
            if response['data']['user']['player'] is None:
                i += 1
                continue

            if i+1 % 35 == 0: # Sleeping so startgg server doesn't hate me
                print("Sleeping for {} seconds".format(sleep_time))
                sleep(sleep_time)

            print("Trying player {}".format(players[i])) # Console logging
            players_info[players[i]] = response['data']['user']

            i += 1 # iteration

    if save_json: # Outputting json file if flag activated
        with open('players.json', 'w+', encoding='utf-8') as outfile:
            json.dump(players_info, outfile, indent=4)

    return players_info
