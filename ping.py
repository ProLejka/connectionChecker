#!/usr/bin/python3

from pingutils import PingUtils
import time
import random

pinger = PingUtils()
sitesArray = pinger.get_all_sites()
loadTick = 0

while pinger.running:
    loadTick += 1
    if loadTick == 60:
        sitesArray = pinger.get_all_sites()
        loadTick = 0
    for site in sitesArray:
        if not pinger.ping_host(site[1]):
            pinger.insert_stat(site[0])
    time.sleep(10 + random.randrange(0, 6))
