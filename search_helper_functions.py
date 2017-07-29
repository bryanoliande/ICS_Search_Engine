import re
import os
from collections import defaultdict
import operator
from operator import itemgetter
import bisect
#from natsort import natsorted, ns
import sys
import json
import pickle
import math
from functools import reduce
from bs4 import BeautifulSoup


# change numbers to actual links
def convert_number_to_link(number):
    with open('/Users/bryanoliande/PycharmProjects/ICSSearchEngine/Bookkeeping/bookkeeping.json', 'r') as fp:
        number_to_link_map = json.load(fp)
    if number in number_to_link_map:
        return number_to_link_map[number]
    else:
        print(str(number) + ' couldnt be translated')
        return 'bookkeepingerror'

# derive a list of stop words from stopwords.txt file
def make_stop_word_list():
    stop_word_file = open('stopwords.txt', 'r')
    stop_word_list = []
    lines = stop_word_file.readlines()
    for line in lines:
        tempList = re.split('[^a-zA-Z0-9]', line)
        for word in tempList:
            if word != '':
                stop_word_list.append(word.lower())
    stop_word_file.close()
    return stop_word_list

def remove_stop_words_from_query(query):
   stop_word_list = make_stop_word_list()
   new_query = ''
   for word in query.split():
        if word not in stop_word_list:
            new_query += (str(word) + ' ')
   return new_query



#return list of (doc, termOccurencesInDoc, termTFIDF)'s or empty list if no results
def get_one_word_results(word, inverted_index_with_tfidf):
    if word in inverted_index_with_tfidf.keys():
        return inverted_index_with_tfidf[word]
    else:
        return []


'''
Document ranking for a query Q with n query words goes:
        documents with n query words appear first,
        then documents with n-1 query words appear next,
        then docs with n-2 query words appear after that,
        ...,
        then docs with only 1 query word appear

    Within each group, docs are sorted by tfidf
'''
def get_query_results(query, inverted_index_with_tfidf):
    all_words_results = []
    unranked_results = []
    ranked_results = []
    document_ids_all_words = []

    for word in query.split():
        word_result = get_one_word_results(word, inverted_index_with_tfidf)
        document_id_single_word = []
        unranked_results += word_result
        for i in range(len(word_result)):
            document_id_single_word.append(word_result[i][0])
        all_words_results.append(word_result)
        document_ids_all_words.append(document_id_single_word)

    for i in range(len(document_ids_all_words)):
        continue

    for i in range(len(all_words_results)):
        continue
    unranked_results = sorted(unranked_results, key=operator.itemgetter(2) , reverse = True)


    #all_word_results now has a list of results for each word. Perform intersection
    #Code taken from: http://stackoverflow.com/questions/3852780/python-intersection-of-multiple-lists
    document_id_intersection = list(reduce(set.intersection, [set(item) for item in document_ids_all_words]))


    already_added_document = []
    #add tuples that are in the intersection
    for item in unranked_results:
        if item[0] in document_id_intersection and item[0] not in already_added_document:
            ranked_results.append(item)
            already_added_document.append(item[0])

    #now append one-word results that aren't in intersection to end list
    #i.e. query is "machine learning" - but some pages only have "machine" or "learning" - wont be in intersection
    for item in unranked_results:
        if item[0] not in document_id_intersection and item[0] not in already_added_document:
            ranked_results.append(item)
            already_added_document.append(item[0])
    return ranked_results