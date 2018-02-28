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
#title          :search_not_title_or_text.py
#description    :To search the query string in titles of articles.
#author         :Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, bjoern.gruening@gmail.com, kiran.telukunta@indiayouth.info
#date           :28-Feb-2018
#usage          :python search_not_title_or_text.py
#=====================================================================================================
#Kersten Doering 17.06.2014

#check http://xapian.org/docs/queryparser.html for syntax and functions

import xappy

if __name__=="__main__":


	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-p", "--xapian_database_path", dest="xapian_database_path", help="Specify the path to the Xapian full text index.", default="xapian/xapian2018")
	parser.add_option("-q", "--querystring", dest="q", help="Supply the query to queried", default="pancreatic colon lung ovarian")
	parser.add_option("-r", "--results_html_name", dest="r", help="name of the results html file (default: Xapian_query_results_NOT.html)", default = "Xapian_query_results_NOT.html")
	parser.add_option("-n", "--number_of_results", dest="n", help="number of results that have to be yielded into specified html file (default: 100)", default = "100")   

	(options, args) = parser.parse_args()

	conn = xappy.SearchConnection(options.xapian_database_path)
	conn.reopen()


	queryString = options.q

	terms = queryString.split(' ')

	#if only one term is given, normal search in title and text field is done
	if len(terms) > 1:
		#the second term is excluded with "AND NOT"
		title = ' AND NOT '.join(terms)
		title = "R115777 AND " + title
		#another example
	#    title = "Erlotinib AND " + title

		text = ' AND NOT '.join(terms)
		text = "R115777 AND " + text
		#another example
	#    text = "Erlotinib AND " + text
	else:
		title, text = queryString, queryString



	title_q = conn.query_field('title', title)
	text_q = conn.query_field('text', text)

	#merge the two NOT-queries for title and text with OR, meaning this should be the case in the title OR the text field
	merged_q = conn.query_composite(conn.OP_OR, [title_q, text_q])
	print "merged search query: ", merged_q

	#save all machting documents in "results" (starting with rank 0 - check help documentation of function "search")
	results = conn.search(merged_q, 0, conn.get_doccount())

	### debug: ###
	##print first 5 examples
	#print "Rank\tPubMed-ID\tTitle (query term highlighted)"
	#for index, result in enumerate(results):
	#    if index > 4:
	#        break
	#    try:
	#        print "%s\t%s\t%s\t%s" % (result.rank, result.id,results.get_hit(index).highlight('title')[0], results.get_hit(index).highlight('text')[0])
	#    except:
	#        print "%s\t%s\t%s\t%s" % (result.rank, result.id,results.get_hit(index).highlight('title')[0], "<i>no abstract</i>")


	#HTML output:
	#open HTML file
	outfile = open("Xapian_query_results_NOT.html","w")
	#document header
	start_string = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html><head>
	<meta http-equiv="content-type" content="text/html; charset=windows-1252">
	<title>Xapian_query_results_NOT</title>
	</head>
	<body>

	<table border="1" width="100%">
	  <tbody><tr>
		<th>Rank</th>
		<th>PubMed-ID</th>
		<th>Title (query term highlighted)</th>
		<th>Abstract (query term highlighted)</th>
	  </tr>
	"""
	#string for finishing HTML document
	end_string = """
	</tbody></table>

	</body></html>
	"""

	#write header
	outfile.write(start_string)
	#write the first 1000 PubMed-IDs and titles with term "pancreatic" or stem "pancreat"
	if int(options.n) > results.matches_estimated:
		print "### Saved first ", results.matches_estimated, "hits of ", results.matches_estimated, " matches in file ", options.r, "###"	
	else:
		print "### Saved first ", options.n, "hits of ", results.matches_estimated, " matches in file ", options.r, "###"

	for index,result in enumerate(results):
		try:
			outfile.write("<tr><td>" + str(index) + "</td><td>" + result.id + "</td><td>" + results.get_hit(index).highlight('title')[0] +"</td><td>" + results.get_hit(index).highlight('text')[0] + "</td></tr>")
		except:
			outfile.write("<tr><td>" + str(index) + "</td><td>" + result.id + "</td><td>" + results.get_hit(index).highlight('title')[0] +"</td><td>" + "<i>no abstract</i>" + "</td></tr>")
		
		if index > (int(options.n) - 1):
			break

	#write string for finishing HTML document
	outfile.write(end_string)
	#close file connection
	outfile.close()
	#close connection to Xapian database


	#searchConn.close()
