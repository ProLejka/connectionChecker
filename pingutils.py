import sqlite3
import subprocess
from os.path import exists
import syslog
import signal


class PingUtils:

    dbconn = None
    db = None
    running = True

    def __init__(self):
        if not self.chceck_db_exist():
            exit()
        self.dbconn = sqlite3.connect('database/ping.db')
        self.db = self.dbconn.cursor()
        self.check_table_exist('sites')
        self.check_table_exist('ping_stats')
        signal.signal(signal.SIGINT, self.shutdown_trigger)
        signal.signal(signal.SIGTERM, self.shutdown_trigger)

    def shutdown_trigger(self, *args):
        self.db.close()
        self.dbconn.close()
        self.running = False

    def chceck_db_exist(self):
        if exists('database/ping.db'):
            return True
        self.running = False
        return False

    def ping_host(self, host):
        command = ['ping', '-c', '1', '-w5',  host]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

    def check_table_exist(self, table_name):
        self.db.execute(
            ''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s' ''' % (table_name))
        if self.db.fetchone()[0] != 1:
            file_path = 'sql/%s.sql' % (table_name)
            if exists(file_path):
                file = open(file_path, 'r')
                sql_table_script = file.read()
                file.close()
                self.db.executescript(sql_table_script)
                self.dbconn.commit()
                return True
            else:
                syslog.syslog(syslog.LOG_ERR, "Can't find %s.sql" %
                              (table_name))
        return False

    def insert_stat(self, site_id):
        try:
            self.db.execute(
                "INSERT INTO ping_stats (site_id) VALUES (?)", (site_id,))
            self.dbconn.commit()
            return True
        except sqlite3.IntegrityError as e:
            syslog.syslog(syslog.LOG_ERR,
                          "Problem with inserting site. ID %s . %s" % site_id, e)
        return False

    def get_all_sites(self):
        sites_in_db = self.db.execute('SELECT * FROM sites')
        return sites_in_db.fetchall()

    def check_if_site_exist(self, site_name):
        sites = self.get_all_sites()
        for site in sites:
            if site_name == site[1]:
                return True
        return False

    def delete_site(self, url):
        if not self.check_if_site_exist(url):
            print('Site is not on list: %s' % url)
            return False
        self.db.execute('DELETE FROM sites WHERE url_addr LIKE ?', (url,))
        self.dbconn.commit()
        print('Site deleted: %s' % url)
        return True

    def add_site(self, url):
        if self.check_if_site_exist(url):
            print('Site is already on list: %s' % url)
            return False
        self.db.execute('INSERT INTO sites (url_addr) VALUES (?)', (url,))
        self.dbconn.commit()
        print('Site added: %s' % url)
        return True
