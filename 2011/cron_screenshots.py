#!/usr/bin/env python

import sqlite3
import subprocess
import urllib, json
import sys, os
import logging
from datetime import datetime

dirname = os.path.dirname(sys.argv[0])

LOG_FILENAME = '%s/screenshots.log' % dirname
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug('Screenshots cron was run on %s !' % str(datetime.now()))

conn = sqlite3.connect('%s/screenshots.sqlite' % dirname)

username, password = 'SETME', 'SETME'
hostname = 'thot.sec-l.org'

try:
     for entry in json.loads(urllib.urlopen('http://%s/webservices/screenshots_queue/' % hostname).read()):
          try:
               c = conn.execute('select count(*) from screenshot where id == %d' % entry['id']);
               if c.fetchone()[0] <= 0:
                    conn.execute("insert into screenshot values (%d, '%s', 0)" % (entry['id'], entry['url']))

          except sqlite3.Error, e:
               print "A error occured:", e.args[0]
     conn.commit()
except:
     print "JSON ERROR"


ok = 0
for entry in conn.execute('select * from screenshot where done == 0').fetchall():
     url = entry[1].replace('http://', 'http://%s:%s@' % (username, password))
     retcode = subprocess.call(["python", "%s/webkit2png.py" % dirname, "-t", "5", "-d", ":8412", "-o",  "/var/www/screenshots/%d.png" % entry[0], "-g", "1024", "768", url]);
     if retcode == 0:
          conn.execute('update screenshot set done = 1 where id = %d' % entry[0])
          conn.commit()
          ok += 1

if ok:
     os.system('/root/screenshot/update_all_thumbs.sh')

conn.commit()
conn.close()

#     print "%s done " % entry['url']
