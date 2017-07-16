import json
import requests
import os
import sys
import time 
import ctypes
import threading
from threading import Thread

currencies = ["bitcoin", "litecoin", "gulden"]
watcher = {"bitcoin": [3000, -1, False], "litecoin": [35, -1, False], "gulden": [100, -1, False]}

def print_row(currency, market_cap, price, change, color = False):
    if color == True and float(change) > 0:
        print ("\x1b[1;32;40m %-30s %-15s %15s %35s \x1b[0m" % (currency, market_cap, price, change))
    elif color == True:
        print ("\x1b[1;31;40m %-30s %-15s %15s %35s \x1b[0m" % (currency, market_cap, price, change))
    else:
        print (" %-30s %-15s %15s %35s" % (currency, market_cap, price, change))

def alert(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

def handle(currency):
    watcher[currency['id']][1] = float(currency['price_usd'])
    print_row (currency['id'], currency['market_cap_usd'], currency['price_usd'], currency['percent_change_24h'], True)

def watch(arg, stop_event):
    while not stop_event.is_set():
        for currency in watcher:
            if watcher[currency][1] >= watcher[currency][0] and watcher[currency][2] == False:
                watcher[currency][2] = True
                alert(currency, "Limit reached !")
               
    time.sleep(2)
try:
    thread_stop = threading.Event()
    thread = Thread(target = watch, args=(1, thread_stop))
    thread.start()
    while 1:
        response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
        assert response.status_code == 200
        os.system('cls')
        print_row ("Currency", "Market Cap", "Price", "% Changes (24h)")
        print_row ("--------------", "--------------", "---------", "--------------")
        for currency in response.json():
            if currency['id'] in currencies:
                handle(currency)
except KeyboardInterrupt:
    print ("Exit...")
    thread_stop.set()
    sys.exit()
