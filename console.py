# -*- coding: utf-8 -*-
#!/usr/bin/python

#console.py

import sys, getopt
from optparse import OptionParser



parser = OptionParser()

parser.add_option("-i", "--input", dest="filename", help="read log from FILE", metavar="INPUT")
parser.add_option("-o", "--output", dest="filename", help="write log to FILE", metavar="OUTPUT")
#parser.add_option("-h", "--help", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()