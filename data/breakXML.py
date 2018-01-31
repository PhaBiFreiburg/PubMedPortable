#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#Kersten Doering 09.07.2014

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

	with open(inFileName, 'r') as inFileFid:
		for lineCounter, line in enumerate(inFileFid):
			if (fileStartTag in line) or (fileEndTag in line):
				continue

			if endTag in line:
				outFileID.write(endTag + '\n')
				documentCounter += 1
				haveStartLine = False
				if documentCounter == noOfDocumentsInOneXML:
					outFileID.write("\n\n" + fileEndTag)
					outFileID.close()
					nextFile = True
					fileNumber += 1
					continue
				

			if nextFile:
				outFileName = outDirectoryName + "medline_" + str(fileNumber) + ".xml"
				outFileID = open(outFileName, 'w')
				outFileID.write(XMLHeader)
				documentCounter = 1
				nextFile = False

			if startTag in line:
				haveStartLine = True
				outFileID.write('\n\n' + startTag + '\n')
				continue

			if haveStartLine:
				outFileID.write(line)



