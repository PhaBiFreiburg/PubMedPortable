#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2018, Kiran Telukunta
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of PubMedPortable nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#==============================================================================
#title			:RESTFul.client.get.py
#description	:RESTful API taken from https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/
#author			:Kiran Telukunta
#email          :kiran.telukunta@indiayouth.info
#date			:1-Apr-2018
#usage			:python3 RESTFul.client.get.py
#==============================================================================

from __future__ import print_function
import urllib2
import time
import sys
import getopt
import sys
import re


class ProgressBar(object):
    DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'

    def __init__(self, total, width=40, fmt=DEFAULT, symbol='=', output=sys.stderr):
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        self.fmt = re.sub(r'(?P<name>%\(.+?\))d', r'\g<name>%dd' % len(str(total)), fmt)
        self.current = 0

    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'
        args = {
            'total': self.total,
            'bar': bar,
            'current': self.current,
            'percent': percent * 100,
            'remaining': remaining
        }
        print('\r' + self.fmt % args, file=self.output, end='')

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)



inputFile = ''
bioconcept = ''
format = ''

try:
	options, remainder = getopt.getopt(sys.argv[1:], 'i:b:f:o:', ['inputfile=','bioconcept=','format=', 'output='])
except getopt.GetoptError as err:
	print("\n python RESTful.client.get.py -i [inputfile] -b [bioconcept] -f [format]\n")
	print("\t bioconcept: We support five kinds of bioconcepts, i.e., Gene, Disease, Chemical, Species, Mutation. When 'BioConcept' is used, all five are included.\n")
	print("\t inputfile: a file with a pmid list\n")
	print("\t format: PubTator (tab-delimited text file), BioC (xml), and JSON\n")
	print("\t output: File name to which output is written\n\n")
	sys.exit(0)
														 
for opt, arg in options:
	if opt in ('-i', '--inputfile'):
		inputFile = arg
	elif opt in ('-b', '--bioconcept'):
		bioconcept = arg
	elif opt in ('-f', '--format'):
		format = arg
	elif opt in ('-o', '--output'):
		outPutFile = arg

fh = open(inputFile)

outPutFH = open(outPutFile, 'w')

downloadProgress = ProgressBar(612508, fmt=ProgressBar.FULL)
skipLines = 46671

for pmid in fh:
	#Submit
	if skipLines > downloadProgress.current:
		next(fh)
		downloadProgress.current += 1
		downloadProgress()
		continue

	pmid = pmid.rstrip('\r\n')
	url_Submit = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + bioconcept + "/" + pmid + "/" + format + "/"
	try:
		urllib_result = urllib2.urlopen(url_Submit)
		outPutFH.write(urllib_result.read())
		downloadProgress.current += 1
		downloadProgress()
	except urllib2.HTTPError:
		time.sleep(120)
		continue
downloadProgress.done()
