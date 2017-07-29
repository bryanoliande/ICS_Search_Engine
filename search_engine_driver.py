import re
import os
from collections import defaultdict
import operator
from operator import itemgetter
import bisect
# from natsort import natsorted, ns
import sys
import json
import pickle
import math
from functools import reduce
from bs4 import BeautifulSoup


import search_helper_functions as search_helper

while True:
    inverted_index_with_tfidf = pickle.load(open('saved_inverted_index_with_tfidf.p', 'rb'))
    query = input('Enter query (type \'quit121\' to quit): ').lower()
    query = search_helper.remove_stop_words_from_query(query).strip()

    if query == 'quit121':
        print('Goodbye!')
        exit(0)
    if query != '':
        list_of_sites = search_helper.get_query_results(query, inverted_index_with_tfidf)
        num_sites_printed = 0
        for i in range(len(list_of_sites)):
            if num_sites_printed > 5:  # only return top five results (CHANGE THIS FOR MORE/LESS)
                break
            url = search_helper.convert_number_to_link(list_of_sites[i][0])
            if 'datasets' in url:
                continue
            print('http://' + url + '\n')
            num_sites_printed = num_sites_printed + 1
        if num_sites_printed == 0:
            print('NO RESULTS FOUND!')
    else:
        print('You entered a bad query! Try again (maybe use less stop words next time)...')