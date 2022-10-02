#!/usr/bin/python3

from pingutils import PingUtils
import time

pinger = PingUtils()
sitesArray = pinger.get_all_sites()
loadTick = 0

pinger.log_sys('Starting checker')

while pinger.running:
    loadTick += 1
    pinger.log_sys('loadtick %s' % loadTick)
    if loadTick == 60:
        sitesArray = pinger.get_all_sites()
        loadTick = 0
    for site in sitesArray:
        pinger.log_sys('pinging %s' % site[1])
        if not pinger.ping_host(site[1]):
            pinger.insert_stat(site[0])
    time.sleep(10)
