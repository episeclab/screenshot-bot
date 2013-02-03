#!/usr/bin/env python

import sqlite3
import subprocess
import json
import urllib, urllib2
import cookielib
import sys, os
import logging
from lxml import html
from datetime import datetime

dirname = os.path.dirname(sys.argv[0])

LOG_FILENAME = '%s/screenshots.log' % dirname
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug('Screenshots cron was run on %s !' % str(datetime.now()))

conn = sqlite3.connect('%s/screenshots.sqlite' % dirname)

username, password = 'esl', 'lkjsdflkjsdf'
hostname = 'thot-dev'
login_url = "http://%s/accounts/login/" % hostname


cj = cookielib.CookieJar()

opener = urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cj)
)

login_form = opener.open(login_url).read()
csrf_token = html.fromstring(login_form).xpath(
    '//input[@name="csrfmiddlewaretoken"]/@value'
)[0]

values = {
    'username': username,
    'password': password,
    'csrfmiddlewaretoken': csrf_token,
}

# Convert to params
params = urllib.urlencode(values)
login_page = opener.open(login_url, params)

try:
     conn.execute('select 1 from screenshot')
except:
     conn.execute('CREATE TABLE screenshot (id PRIMARY KEY, url TEXT, done INTEGER)')
try:
     for entry in json.loads(opener.open('http://%s/webservices/screenshots_queue/' % hostname).read()):
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
     os.system('%s/update_all_thumbs.sh' % dirname)

conn.commit()
conn.close()
