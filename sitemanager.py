#!/usr/bin/python3

from pingutils import PingUtils
import sys

pinger = PingUtils()
params = sys.argv
del params[0]
deleteFlag = False

if params[0] == 'help':
    print(''' Usage:
    help - this help
    list - list of sites
    add param1 ... paramN - add site(s) to db
    remove param1 ... paramN  - remove site(s) from db ''')
    exit()

if params[0] == 'list':
    sitesArray = pinger.get_all_sites()
    for site in sitesArray:
        print(site[1])
    exit()

if params[0] == 'remove':
    deleteFlag = True
    del params[0]

if params[0] == 'add':
    del params[0]

for argument in params:
    if deleteFlag:
        pinger.delete_site(argument)
    else:
        pinger.add_site(argument)
