#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Kersten Doering, Kiran Telukunta
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
#description    :This script downloads PubMed-IDs and country names of journals from a PostgreSQL database and generates a PNG file with a pie chart showing the amount of publications in percent. Therefore, this plot shows the amount of publications per country in terms of the journal origin (publisher), but not in terms of authors or institutes.
#author         :Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, kiran.telukunta@indiayouth.info
#date           :28-Feb-2018
#usage          :python search_title_or_text.py
#=====================================================================================================

# Kersten Doering 27.01.2015

import matplotlib.pyplot as plt

"""
SQL command to get data (this entry is not set for every PubMed-ID) - this data set is based on the download of XML files from 16th April 2015 (23258 PubMed-IDs):
\copy (select fk_pmid, lower(country) from pubmed.tbl_medline_journal_info where country is not null order by country asc) to 'countries_pancreatic_cancer.csv' delimiter ','
"""

#create a dictionary with key country name and value amount of publications
import xappy
if __name__=="__main__":


	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-i", "--countries_input", dest="i", help="Specify the countries input file obtained from the SQL countries Query.", default="countries_pancreatic_cancer.csv")
	parser.add_option("-o", "--pie_output", dest="o", help="Specify the output image file name for the pie chart to be generated.", default="pie_chart_countries_publications.png")
	parser.add_option("-r", "--rest_countries", dest="r", help="Specify the percentage limitation to count into others category.", default="2.0")

	(options, args) = parser.parse_args()

	countries = {}
	infile = open(options.i,"r")
	for line in infile:
		country = line.strip().split(",")[1]
		if not country in countries:
			countries[country] = 1
		else:
			countries[country] += 1
	infile.close()

	# parameters for the plot
	# labels and sizes are mandatory
	labels = []
	sizes = []
	# fractions below 2 % are not taken into account within the plot, but saved
	rest_labels = []
	rest_sizes = []
	# fixed colors for fractions (optional)
	colors = ['yellowgreen', 'red', 'lightblue', 'lightcoral', 'green', 'lightskyblue', 'gold', 'lightgrey', 'orange', 'grey']

	# total sum of publications to calculate percentages
	size_sum = float(sum(countries.values()))
	# sort dictionary by amount of publications per country
	# (http://stackoverflow.com/questions/16772071/sort-dict-by-value-python)
	list_sorted = sorted(countries.items(), key=lambda x:x[1])

	#for country,amount in countries.items():
	for country,amount in list_sorted:
		size = (float(amount)/size_sum)*100.0
		if size < float(options.r):
			 # debug:
	#        print country,size
			rest_sizes.append(size)
			rest_labels.append(country)
		else:
			 # debug:
	#        print country,size
			sizes.append(size)
			# capitalize country names
			labels.append(country.title())
	# add fraction for "Others" (below 2 %)
	rest_size = sum(rest_sizes)
	sizes.append(rest_size)
	labels.append("Others\n(< 2 %)")
	# size of figure
	plt.figure(figsize=(11,8.5))
	# plot with parameters
	plt.pie(sizes, labels=labels,autopct='%1.1f%%',pctdistance = 1.1,labeldistance = 1.2, radius = 5,shadow = True, colors=colors)
	# comment from the matplotlib example: 
	# (http://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')

	# show on screen
	#plt.show()

	# save plot
	plt.savefig(options.o)

