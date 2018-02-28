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
#title          :search_title_or_text.py
#description    :To search the query string in titles or text of articles.
#author         :Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, bjoern.gruening@gmail.com, kiran.telukunta@indiayouth.info
#date           :28-Feb-2018
#usage          :python search_title_or_text.py
#=====================================================================================================

#Kersten Doering 16.06.2014

#check https://github.com/miracle2k/xappy/blob/master/docs/introduction.rst for nice examples

import xappy
if __name__=="__main__":


	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-p", "--xapian_database_path", dest="xapian_database_path", help="Specify the path to the Xapian full text index.", default="xapian/xapian2018")
	parser.add_option("-q", "--querystring", dest="q", help="Supply the query to queried", default="R115777")
	parser.add_option("-r", "--results_html_name", dest="r", help="name of the results html file (default: Xapian_query_results_OR.html)", default = "Xapian_query_results_OR.html")
	parser.add_option("-n", "--number_of_results", dest="n", help="number of results that have to be yielded into specified html file (default: 100)", default = "100")   

	(options, args) = parser.parse_args()

	searchConn = xappy.SearchConnection(options.xapian_database_path)
	searchConn.reopen()



	#########################

	querystring = options.q
	#another example:
	#querystring = "pancreatic cancer" #also searches for "pancreat" and "cancers"
	#use phrase search to get only exact hits

	title, text, keyword = querystring, querystring, querystring

	title_q = searchConn.query_field('title', title)
	text_q = searchConn.query_field('text', text)
	#other fields are possible:
	#keyword_q = searchConn.query_field('keyword', keyword)

	print "search query title: ", title_q
	print "search query text: ", text_q
	#other fields are possible:
	#print "search query keyword: ", keyword_q

	merged_q = searchConn.query_composite(searchConn.OP_OR, [title_q, text_q])#, keyword_q])#other fields are possible:
	print "merged search query: ", merged_q


	#save all machting documents in "results" (starting with rank 0 - check help documentation of function "search")
	results = searchConn.search(merged_q, 0, searchConn.get_doccount())


	### debug: ###
	##print first 5 titles with highlight function and save first 1000 titles in an HTML file
	#print "Rank\tPubMed-ID\tTitle (query term highlighted)"
	#for index,result in enumerate(results):
	#    if index > 4:
	#        break
	#    try:
	#        print "%s\t%s\t%s\t%s" % (result.rank, result.id,results.get_hit(index).highlight('title')[0], results.get_hit(index).highlight('text')[0])
	#    except:
	#        print "%s\t%s\t%s\t%s" % (result.rank, result.id,results.get_hit(index).highlight('title')[0], "<i>no abstract</i>")


	#open HTML file
	outfile = open(options.r,"w")
	#document header
	start_string = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html><head>
	<meta http-equiv="content-type" content="text/html; charset=windows-1252">
	<title>Xapian_query_results OR</title>
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
