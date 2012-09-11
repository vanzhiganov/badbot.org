# -*- coding: utf-8 -*-
import sys
import os
import datetime
import re
import apachelog
from base64 import b64encode
import requests

# STEP 0. ...
url = 'http://badbot.org/report.php'
hash = '1234123k4h132jk4h123kj4h123kj4h2k13j4h'
fileApacheLog = '/var/log/apache2/error.log'
# path to pid-file
filePid = 'testsyncDemon.pid'
# path to log-file
fileLog = 'testStoreTask.log'
# program start time (not used, but it may need any time)
dateStart = datetime.datetime.now()

reqtoken = 'secretRequestTokenForRPC'
resToken = 'secretResponseTokenForRPC'
rpcLink = "http://s.nazya.com/rpc/"

# STEP 1. Open log file
log_file = open(fileLog, 'a+')

# STEP 2. Check exists pid-file
if os.path.exists(filePid):
        # read pid-file
        f = open(filePid, 'r')
        readPid = f.read()
else:
        readPid = '-100'

print '[{0}] - pid:{1} - start and check'.format(datetime.datetime.now(), readPid)

# STEP 3. Check process by PID from PID-file
try:
        os.kill(int(readPid), 0)
        workerStarted = True
except:
        workerStarted = False

# STEP 4. If 
if workerStarted :
#        print os.getpid()
        print '[{0}] - pid:{1} - already started, STOP PROGRAM'.format(datetime.datetime.now(), readPid)
        sys.exit(0)
else :
        # get current PID
        pid = os.getpid()
        print '[{0}] - pid:{1} - not started, ATTENTION! Program continues with new PID: {2}'.format(datetime.datetime.now(), readPid, pid)
        readPid = pid
        # write PID to file
        f = open(filePid, 'w')
        f.write(str(pid))
        f.close()

# STEP 5. Work with Worker ...  
print '[{0}] - pid:{1} - start work with worker'.format(datetime.datetime.now(), readPid)

############
# Format copied and pasted from Apache conf - use raw string + single quotes
format = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

p = apachelog.parser(format)

for line in open('/var/log/apache2/access.log'):
    try:
       data = p.parse(line)
       
       
       
       post_data = {"hash":hash, "host":b64encode(data['%h']), "useragent":b64encode(data['%{User-Agent}i']),"time":b64encode(data['%t'])}
       #print 'hash={0};host:{1};useragent:{2};time:{3}'.format(hash,b64encode(data['%h']),b64encode(data['%{User-Agent}i']),b64encode(data['%t']))
       print data
       #print data['%{User-Agent}i']
       
#       for s in data:
#           print s[l]
       
    except:
       sys.stderr.write("Unable to parse %s" % line)

