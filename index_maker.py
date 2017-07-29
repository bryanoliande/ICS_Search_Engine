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

import index_helper_functions as index_helper

rootdir = '/Users/bryanoliande/PycharmProjects/ICSSearchEngine/WEBPAGES_SIMPLE'
term_dict = index_helper.make_token_sequence(rootdir)
specialdict = index_helper.make_special_token_sequence(rootdir)
pickle.dump(specialdict, open('specialdict.p', 'wb'))
inverted_index = index_helper.make_inverted_index(term_dict)
pickle.dump(inverted_index, open('saved_inverted_index.p', 'wb'))
inverted_index_with_tfidf = index_helper.make_inverted_index_with_tf_idf(inverted_index)
pickle.dump(inverted_index_with_tfidf, open('saved_inverted_index_with_tfidf.p', 'wb'))