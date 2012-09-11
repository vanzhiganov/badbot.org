# -*- coding: utf-8 -*-
import sys
import os
import datetime
import re
import apachelog
from base64 import b64encode
import requests

# git push origin master

# STEP 0. ...
reposrturl = 'http://badbot.org/report.php'
hash = '1234123k4h132jk4h123kj4h123kj4h2k13j4h'
fileApacheLog = '/var/log/apache2/error.log'
pathApacheLog = '/var/log/apache2'
# path to pid-file
filePid = '/tmp/badbot.pid'
# path to log-file
fileLog = '/var/log/badbot.log'
# program start time (not used, but it may need any time)
dateStart = datetime.datetime.now()

# STEP 1. Open log file
log_file = open(fileLog, 'a+')

# STEP 2. Check exists pid-file
if os.path.exists(filePid):
        # read pid-file
        f = open(filePid, 'r')
        readPid = f.read()
else:
        readPid = '-100'

print '[{0}] - pid:{1} - start program'.format(datetime.datetime.now(), readPid)

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

# STEP 5.1. read apache log dir
for pathApacheLog, subFolders, files in os.walk(pathApacheLog):
    for file in files:
        ext = os.path.splitext(pathApacheLog+'/'+file)[1]
        
        if ext == '.log':
            print '[{0}] - pid:{1} - read log-file: {2}'.format(datetime.datetime.now(), readPid, pathApacheLog+'/'+file)
            currlogfile = pathApacheLog+'/'+file
            #print pathApacheLog+'/'+file

            # STEP 5.2. parse log file
            ############
            # Format copied and pasted from Apache conf - use raw string + single quotes
            format = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
            p = apachelog.parser(format)

            # Common Log Format (CLF)
            #p = apachelog.parser(apachelog.formats['common'])
            
            # Common Log Format with Virtual Host
            #p = apachelog.parser(apachelog.formats['vhcommon'])
            
            # NCSA extended/combined log format
            #p = apachelog.parser(apachelog.formats['extended'])
            
            for line in open(currlogfile):
                try:
                    data = p.parse(line)
            
                    post_data = {"hash":hash, "host":b64encode(data['%h']), "useragent":b64encode(data['%{User-Agent}i']),"time":b64encode(data['%t'])}
            
                    #if data['%{User-Agent}i'] == "ZmEu":
                    r = requests.post(reposrturl, post_data)
                    #print r.status_code
                    #print r.headers['content-type']
                    print '[{0}] - pid:{1} - [send] - host:{2} - useragent:{3} - time:{4}'.format(datetime.datetime.now(), readPid, data['%h'], data['%{User-Agent}i'], data['%t'])
                except:
                   sys.stderr.write("Unable to parse %s" % line)

print '[{0}] - pid:{1} - stop program'.format(datetime.datetime.now(), readPid)