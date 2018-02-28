#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Kersten Doering, Bjoern Gruening, Kiran Telukunta
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

#======================================================================================================
#title			:search_near_title.py
#description	:To search the query strings near the titles of articles.
#author			:Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, bjoern.gruening@gmail.com, kiran.telukunta@indiayouth.info
#date			:28-Feb-2018
#usage			:python search_near_title.py
#=====================================================================================================
#Kersten Doering 16.06.2014

#check http://xapian.org/docs/queryparser.html for syntax and functions

import xappy

if __name__=="__main__":


	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-p", "--xapian_database_path", dest="xapian_database_path", help="Specify the path to the Xapian full text index.", default="xapian/xapian2018")
	parser.add_option("-a", "--querystring1", dest="a", help="Supply the first query to queried", default="pancreatic cancer")
	parser.add_option("-b", "--querystring2", dest="b", help="Supply the second query to queried", default="Erlotinib")
	parser.add_option("-r", "--results_html_name", dest="r", help="name of the results html file (default: Xapian_query_results_NEAR.html)", default = "Xapian_query_results_NEAR.html")
	parser.add_option("-n", "--number_of_results", dest="n", help="number of results that have to be yielded into specified html file (default: 1000)", default = "1000")	

	(options, args) = parser.parse_args()

	searchConn = xappy.SearchConnection(options.xapian_database_path)
	searchConn.reopen()
	#########################

	querystring1 = options.a
	querystring2 = options.b

	#in the following example, "pancreatic cancer" and "Erlotinib" are not allowed to have more than 4 other words between them"
	#"title" and "text" are searched with Xapian

	#"pancreatic cancer" is split into two terms and connected with the other query using "NEAR"
	terms = querystring1.split(' ')
	querystring1 = " NEAR/3 ".join(terms)#not more than 2 words are allowed to be between "pancreatic" and "cancer"

	#NEAR searches without considering the word order, while in case of ADJ the word order is fixed
	title = querystring1 + " NEAR/5 " + querystring2#adjusting the limit of words between the terms changes the results

	#same query can be done for the field "text" which is the PubMed abstract and both query fields can be connected with logical OR - look at search_title_or_text.py or search_not_title_or_text.py
	#notice that this becomes a phrase search now for the single terms
	title_q = searchConn.query_field('title', title)


	print "search query: ", title_q

	#save all machting documents in "results" (starting with rank 0 - check help documentation of function "search")
	results = searchConn.search(title_q, 0, searchConn.get_doccount())

	### debug: ###
	#print "Rank\tPubMed-ID\tTitle (query term highlighted)"
	#for index,result in enumerate(results):
	#    if "<b>" in results.get_hit(index).highlight('title')[0]:
	#        print index, "\t", result.id, "\t", results.get_hit(index).highlight('title')[0]
	#    else:
	#        print resuld.id, "does not contain a highlighted term"
	##        if index > 5:
	##            break

	#HTML output:
	#open HTML file
	outfile = open(options.r,"w")
	#document header
	start_string = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html><head>
	<meta http-equiv="content-type" content="text/html; charset=windows-1252">
	<title>Xapian_query_results_NEAR</title>
	</head>
	<body>

	<table border="1" width="100%">
	  <tbody><tr>
		<th>Rank</th>
		<th>PubMed-ID</th>
		<th>Title (query term highlighted)</th>
	  </tr>
	"""
	#string for finishing HTML document
	end_string = """
	</tbody></table>

	</body></html>
	"""

	#write header
	outfile.write(start_string)
	if int(options.n) > results.matches_estimated:
		print "### Saved first ", results.matches_estimated, "hits of ", results.matches_estimated, " matches in file ", options.r, "###"	
	else:
		print "### Saved first ", options.n, "hits of ", results.matches_estimated, " matches in file ", options.r, "###"
	#write the first 1000 PubMed-IDs and titles with term "pancreatic" or stem "pancreat"
	for index,result in enumerate(results):
		outfile.write("<tr><td>" + str(index) + "</td><td>" + result.id + "</td><td>" + results.get_hit(index).highlight('title')[0] +"</td></tr>")
		if index > (int(options.n) - 1):
			break
	#write string for finishing HTML document
	outfile.write(end_string)
	#close file connection
	outfile.close()
	#close connection to Xapian database


	#searchConn.close()
