#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
#title          :generate_surrounding_words_log.py
#description    :Generates the surrounding words log for the given search term
#author         :Kersten Doering, Bjoern Gruening, Kiran Telukunta
#email          :kersten.doering@gmail.com, bjoern.gruening@gmail.com, kiran.telukunta@indiayouth.info
#date           :28-Feb-2018
#usage          :python generate_surrounding_words_log.py
#=====================================================================================================

#Kersten Doering 29.11.2014, major change 03.02.2015

# ToDo: replace whitespace tokenization with a tokenizer that also removes punctuation

# to sort dictionary
from operator import itemgetter
# to calculate logarithm
import math
# to connect to a PostgreSQL relational database
import psycopg2
# to use DictCursor
from psycopg2 import extras
import time
# to use command-line parameters
from optparse import OptionParser
# to join paths
import os


# join abstract title and text for a given PubMed-ID "pmid" and return the triple as a list [PubMed-ID, title, text]
def get_title_text(pmid):
    stmt = """
    SELECT 
        pmid,
        article_title as title,
        abstract_text as abstract
    FROM 
        pubmed.tbl_medline_citation
            LEFT OUTER JOIN
        pubmed.tbl_abstract
                ON pmid = fk_pmid
    WHERE
        pmid = '"""+pmid+"""'
    ;
    """

    cursor.execute(stmt)
    output = cursor.fetchone()
    return output

# main
if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-d", "--database", dest="d", help='name of the database to connect to', default="pancreatic_cancer_db")
    parser.add_option("-x", "--xapian_path", dest="x", help='path to the directory containing the PubMedPortable scripts for generating the Xapian full text index',default="../../full_text_index_title_text")
    parser.add_option("-p", "--pmids_input", dest="p", help='name of the input file that contains all PubMed-IDs for the search term', default="results/results.csv")
    parser.add_option("-t", "--terms_input", dest="t", help='name of the input file that contains all search terms that should not be written to the output file', default="synonyms/pancreatic_cancer.txt")
    parser.add_option("-s", "--stop_words_input", dest="s", help='name of the input file with all stop words that should not be written to the output file', default="blacklist/stop_words.txt")
    parser.add_option("-a", "--search_term", dest="a", help='search term for which most frequently co-occurring words in texts', default="Gemcitabine")
    parser.add_option("-o", "--output", dest="o", help='name of the output file with the most frequently co-occurring words in texts that contain the search term gemcitabine', default="counts_surrounding_words_log.csv")
    (options, args) = parser.parse_args()

    # settings for psql connection
    postgres_user       = "parser"
    postgres_password   = "parser"
    postgres_host       = "localhost" 
    postgres_port       = "5432"
    postgres_db         = options.d
    connection          = psycopg2.connect("dbname='"+postgres_db+"' user='"+postgres_user+"' host='"+postgres_host+"' password='"+postgres_password+"' port='"+postgres_port+"'")
    cursor              = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # save file paths in an extra variable
    pmids_input         = options.p
    terms_input         = options.t
    stop_words_input    = options.s
    output              = options.o
    xapian_path         = options.x
    search_term         = options.a

    # results from RunXapian.py - save  PubMed-IDs in list pmids:
    pmids = []
    infile = open(os.path.join(xapian_path, pmids_input),"r")
    for line in infile:
        temp_line = line.strip().split("\t")
        if temp_line[1] == search_term:
            pmids.append(temp_line[0])
    infile.close()
    # make list unique:
    pmids = list(set(pmids))

    # search terms for RunXapian.py - save in list search_terms:
    search_terms = []
    infile = open(os.path.join(xapian_path, terms_input),"r")
    for line in infile:
        search_terms.append(line.strip().lower())
    infile.close()

    # get stop words, but not comment lines (starting with "#") or empty lines:
    stop_words = []
    infile = open(os.path.join(xapian_path, stop_words_input),"r")
    for line in infile:
        if line.startswith("#") or line.startswith("\n"): 
            # go to next line
            continue
        else: 
            stop_words.append(line.strip())

    # total list of terms as result from whitespace tokenization
    total_list = []
    # iterate over all PubMed-IDs
    for pmid in pmids:
        # get the triple [PubMed-ID, title, text]
        pmid_title_text = get_title_text(pmid)
        # pmid_title_text[0] equals pmid
        # title equals pmid_title_text[1]
        # text equals pmid_title_text[2]
        text = pmid_title_text[2]
        #some PubMed-IDs do not have an abstract text
        if text:
            abstract = pmid_title_text[1] + " " + text
        else:
            abstract = pmid_title_text[1]
        # use a new variable temp_list for every abstract for accepted terms
        temp_list = []
        # whole text splitted into single terms:
        split_list = abstract.split(" ")

        # iterate over all terms in an abstract:
        for elem in split_list:
            # exclude stop words and words with only 3 characters
            if not elem.lower() in stop_words and not len(elem) < 4:
                #r emove punctuation that appears most frequently: 
                if elem[-1] == "," or elem[-1] == "." or elem[-1] == ":":
                    elem = elem[:-1]
                # exclude terms that were searched for in the PubMedPortable documentation
                if not elem.lower() in search_terms:
                    temp_list.append(elem.lower()) 
        # add temp_list to the complete list of splitted terms
        total_list += temp_list
    # make list unique
    total_set = set(total_list)

    # create a dictionary that contains the frequencies of each term
    total_dict = {}
    for elem in total_list:
        if not elem in total_dict:
            total_dict[elem] = 1
        else:
            total_dict[elem] += 1
    # sorted by frequencies
    total_sorted = sorted(total_dict.items(), key=itemgetter(1), reverse = True)

    # save the first 50 terms in a CSV file
    outfile = open(output,"w")
    counter = 0
    for synonyms in total_sorted:
            if counter == 50:
                break
            # use logarithmic scaling
            outfile.write(str(synonyms[0])+"\t"+str(int(math.log(synonyms[1],10)))+"\n")
            counter += 1
    outfile.close()

