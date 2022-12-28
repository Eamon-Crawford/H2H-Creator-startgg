import events
import players
from dotenv import load_dotenv
from os import getenv

import json

class H2HMaker(object):
    def __init__(self, key, save_json:bool, sleep_time=15): # Initializes object
        self.key = key
        self.header = {"Authorization": "Bearer " + key}
        self.save_json = save_json
        self.sleep_time = 10 # Sleep time is how long it waits between 6 queries to sleep

    def set_key(self, new_key): # Sets new key
        self.key = new_key
        self.header = {"Authorization": "Bearer " + new_key}

    def set_sleep_time(self, new_sleep_time):
        self.sleep_time = new_sleep_time

    def set_save_json(self, new_save_json):
        self.save_json = new_save_json

    def print_key(self):
        print(self.key)
    
    def print_header(self):
        print(self.header)

    def print_sleep_time(self):
        print(self.sleep_time)
        
    def get_events(self, tournaments:list, game:int):
        return events.get_events(tournaments, game, self.save_json, self.header)

    def get_results(self, tournaments:list, game:int): # Don't know if will be implemented
        return

    def create_h2h_spreadsheet(self, players:list, tournaments:list, game:int):
        return

def main():
    # Testing area
    load_dotenv()
    key = getenv("KEY")
    test = H2HMaker(key, True)

    data = test.get_events(["genesis-8"], 1)

    print(json.dumps(data, indent=4))

main()