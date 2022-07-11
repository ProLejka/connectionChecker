#!/usr/bin/python

import sqlite3
from os.path import exists
import pingutils
import sys

if not exists('database/ping.db'):
    exit()

dbconn = sqlite3.connect('database/ping.db')
pingutils.check_table_exist(dbconn, 'sites')
pingutils.check_table_exist(dbconn, 'ping_stats')

params = sys.argv
del params[0]
deleteFlag = False

db = dbconn.cursor()

if params[0] == 'help':
    print(''' Usage:
    help - this help
    list - list of sites
    add param1 ... paramN - add site(s) to db
    remove param1 ... paramN  - remove site(s) from db ''')
    exit()

if params[0] == 'list':
    sitesArray = pingutils.get_all_sites(db)
    for site in sitesArray:
        print(site[1])
    exit()

if params[0] == 'remove':
    deleteFlag = True;
    del params[0]

if params[0] == 'add':
    del params[0]

for argument in params:
    siteExist = pingutils.check_if_site_exist(db, argument)
    if deleteFlag:
        if not siteExist:
            print('Site is not on list: %s'  % (argument))
            continue
        db.execute('DELETE FROM sites WHERE url_addr LIKE ?', (argument,))
        print('Site deleted: %s'  % argument)
    else:
        if siteExist:
            print('Site is already on list: %s'  % (argument))
            continue
        db.execute('INSERT INTO sites (url_addr) VALUES (?)', (argument,))
        print('Site added: %s'  % argument)
    dbconn.commit()


db.close()
dbconn.close()
