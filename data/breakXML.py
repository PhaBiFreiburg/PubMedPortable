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
#title			:breakXML.py
#description	:To break combined XML file into defined number of parts
#author			:Kiran Telukunta
#email          :kiran.telukunta@indiayouth.info
#date			:1-Feb-2018
#usage			:python3 breakXML.py
#==============================================================================

if __name__=="__main__":

	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-s", "--size", dest="s", help='Number of documents in one XML file in a file default is 100', default=100)
	parser.add_option("-f", "--file", dest="f", help="name of the input file with a list of documents", default = "pancreatic_cancer_example/medline_00000000.xml")
	parser.add_option("-d", "--directory", dest="d", help="name of the directory in which the files should be saved", default = "pancreatic_cancer")
	
	(options, args) = parser.parse_args()
	
	#save parameters in an extra variable
	noOfDocumentsInOneXML = int(options.s)
	inFileName = options.f
	outDirectoryName = options.d

	XMLh1 = "<?xml version=\"1.0\"?>"
	XMLh2 = "<!DOCTYPE PubmedArticleSet PUBLIC \"-//NLM//DTD PubMedArticle, 1st January 2018//EN\" \"https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_180101.dtd\">"
	fileStartTag = "<PubmedArticleSet>"
	XMLHeader = XMLh1 + "\n" + XMLh2 + "\n" + fileStartTag + "\n"

	nextFile = True
	fileNumber = 1
	documentCounter = 0

	startTag = "<PubmedArticle>"
	endTag = "</PubmedArticle>"
	fileEndTag = "</PubmedArticleSet>"

	haveStartLine = False
	lastFileWritingDone = False

	outFileID = ""

	with open(inFileName, 'r') as inFileFid:
		for lineCounter, line in enumerate(inFileFid):
			if (fileStartTag in line) or (fileEndTag in line):
				continue

			if endTag in line:
				outFileID.write(endTag + '\n')
				haveStartLine = False
				if documentCounter == noOfDocumentsInOneXML:
					outFileID.write("\n\n" + fileEndTag)
					outFileID.close()
					nextFile = True
					fileNumber += 1
					lastFileWritingDone = True
					continue
				documentCounter += 1
				
			if nextFile:
				outFileName = outDirectoryName + "medline_" + str('{:09d}'.format(fileNumber)) + ".xml"
				outFileID = open(outFileName, 'w')
				outFileID.write(XMLHeader)
				documentCounter = 1
				nextFile = False

			if startTag in line:
				haveStartLine = True
				lastFileWritingDone = False
				outFileID.write('\n\n' + startTag + '\n')
				continue

			if haveStartLine:
				outFileID.write(line)


if not lastFileWritingDone:
	outFileID.write("\n\n" + fileEndTag)
	outFileID.close()

