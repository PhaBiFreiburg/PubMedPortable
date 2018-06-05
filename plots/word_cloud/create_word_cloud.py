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
#title          :create_word_cloud.py
#description    :This script creates a word cloud based on a list of words and their frequencies.
#author         :Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, bjoern.gruening@gmail.com, kiran.telukunta@indiayouth.info
#date           :3-Mar-2018
#usage          :python create_word_cloud.py
#=====================================================================================================

#Kersten Doering 29.11.2014, major change 03.02.2015
# inspired by https://github.com/atizo/PyTagCloud/blob/master/pytagcloud/test/tests.py

# PyTagCloud modules
from pytagcloud import create_tag_image, make_tags
# to use command-line parameters
from optparse import OptionParser

# main
if __name__=="__main__":
	parser = OptionParser()
	parser.add_option("-i", "--input", dest="i", help='name of the input file that contains the logarithmic frequencies of each search term, e.g. "counts_surrounding_words_log.csv" or "counts_search_terms_log.csv"')
	parser.add_option("-o", "--output", dest="o", help='name of the output file which contains the word cloud, e.g. "cloud_surrounding_words.png" or "cloud_search_terms.png"')
	parser.add_option("-v", "--ignore_values", dest="v", help='Ignore values which are lesser than specified value, e.g. 0, which will ignore all terms with 0 or less than 0 log value')
	(options, args) = parser.parse_args()

	# no defaults set, show help message if no file names are given
	# use pairs "counts_surrounding_words_log.csv" and "cloud_surrounding_words.png" or "counts_search_terms_log.csv" and "cloud_search_terms.png"
	if not options.i or not options.o:
		parser.print_help()
	else:
		# save file names in an extra variable
		input_file = options.i
		output_file = options.o

		# Ignore values which are lesser than specified value
		if options.v:
			ignoreValueSpecified = True
			ignoreValue = int(options.v)
		else:
			ignoreValueSpecified = False

		# save terms from CSV file in a list and convert their Floats to Integeters
		infile = open(input_file,"r")
		tag_list = []
		for line in infile:
			temp_line = line.strip().split("\t")
			if ignoreValueSpecified:
				if int(float(temp_line[1])) <= ignoreValue:
					continue
			tag_list.append((temp_line[0],(int(float(temp_line[1])))))

		# generate colour and size parameters for each term
		mtags = make_tags(tag_list, maxsize=40)

		nameCounter = 0

		nameCounter += 1 
		output_file = output_file[:-4] + '_' + str(nameCounter) + output_file[-4:]
		create_tag_image(mtags, output_file,size=(1600, 1200),background=(255, 255, 255, 255))


		# nameCounter += 1 
		# output_file = output_file.replace(str(nameCounter-1),str(nameCounter))
		# create_tag_image(mtags, output_file,size=(1800, 1400),background=(255, 255, 255, 255), fontname='Cuprum')
		
		# nameCounter += 1 
		# output_file = output_file.replace(str(nameCounter-1),str(nameCounter))
		# create_tag_image(mtags, output_file,size=(1600, 1000),background=(255, 255, 255, 255), fontname='Inconsolata')

		# nameCounter += 1 
		# output_file = output_file.replace(str(nameCounter-1),str(nameCounter))
		# create_tag_image(mtags, output_file,size=(600, 400),background=(255, 255, 255, 255), fontname='Lobster')
		
		
		# nameCounter += 1 
		# output_file = output_file.replace(str(nameCounter-1),str(nameCounter))
		# create_tag_image(mtags, output_file,size=(700, 500),background=(255, 255, 255, 255), fontname='Neucha')
		
		# nameCounter += 1 
		# output_file = output_file.replace(str(nameCounter-1),str(nameCounter))
		# create_tag_image(mtags, output_file,size=(800, 1300),background=(255, 255, 255, 255), fontname='Neuton')
		
		infile.close()

