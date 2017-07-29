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

#code taken from
#http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(l):
   # print('natural_sort func l = ')
    #print(l)
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

#code taken from
#http://stackoverflow.com/questions/6849047/naturally-sort-a-list-of-alpha-numeric-tuples-by-the-tuples-first-element-in-py
def sorted_nicely(l, key):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]
    return sorted(l, key = alphanum_key)

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

def make_token_sequence(rootdir):
    term_mapping = []  # (term, document_id)
    term_dict = {}
    stop_word_list = make_stop_word_list()

    # took the loopcode from:
    # http: // stackoverflow.com / questions / 10377998 / how - can - i - iterate - over - files - in -a - given - directory
    for subdir, dirs, files in os.walk(rootdir):
        files = natural_sort(files)
        print('# Of Documents: ')
        print(len(files) - 1) #not counting .DS_Store
        for file in files:
            filepath = subdir + os.sep + file
            document_id = filepath.split('WEBPAGES_SIMPLE/', 1)[1]
            if document_id == '.DS_Store' or document_id == '0/.DS_Store':
                continue
            text_file = open(filepath, 'r', encoding='ascii', errors='ignore')
            lines = text_file.readlines()
            doc_word_list = []
            for line in lines:
                tempList = re.split('[^a-zA-Z0-9]', line)
                for word in tempList:
                    if word != '' and word not in doc_word_list and word not in stop_word_list:
                        doc_word_list.append(word.lower())
            for word in doc_word_list:
                term_mapping.append([word, document_id])

                if (word,document_id) in term_dict:
                    term_dict[(word, document_id)] += 1
                else:
                    term_dict[(word, document_id)] = 1

    dict_file = open('dict.txt', 'w+')
    for key in sorted(term_dict):
        dict_file.write('%s: %s \n' % (key, term_dict[key]))
    dict_file.close()
    return term_dict


#finds all special (bold, title, italicized, underlined, etc) words
def make_special_token_sequence(rootdir):
    term_mapping = []  # (term, document_id)
    term_dict = {}
    stop_word_list = make_stop_word_list()

    # took the loopcode from:
    # http: // stackoverflow.com / questions / 10377998 / how - can - i - iterate - over - files - in -a - given - directory
    for subdir, dirs, files in os.walk(rootdir):
        files = natural_sort(files)
        print('# Of Documents: ')
        print(len(files) - 1) #not counting .DS_Store
        for file in files:
            filepath = subdir + os.sep + file
            document_id = filepath.split('WEBPAGES_SIMPLE/', 1)[1]
            if document_id == '.DS_Store' or document_id == '0/.DS_Store':
                continue
            specialword_list = []
            soup = BeautifulSoup(open(filepath, "r", encoding='ascii', errors='ignore'))
            for i in soup.findAll('a'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('b'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('cite'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('em'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('i'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('strong'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('title'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('u'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h1'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h2'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h3'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h4'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h5'):
                for word in i.text.split():
                    specialword_list.append(word)
            for i in soup.findAll('h6'):
                for word in i.text.split():
                    specialword_list.append(word)

            for word in specialword_list:
                if word not in stop_word_list:
                    term_mapping.append([word, document_id])
                    if (word,document_id) in term_dict:
                        term_dict[(word, document_id)] += 1
                    else:
                        term_dict[(word, document_id)] = 1
                else:
                    #print('word ' + str(word) + ' in stop list!')
                    continue

    specialsequence_file = open('specialsequence.txt', 'w+')
    #took sorting code from http://stackoverflow.com/questions/5212870/sorting-a-python-list-by-two-criteria
    term_mapping = sorted(term_mapping, key=operator.itemgetter(0,1))
    for tuple in term_mapping:
        specialsequence_file.write(str(tuple) + '\n')
    specialsequence_file.close()
    specialdict_file = open('specialdict.txt', 'w+')

    for key in sorted(term_dict):
        specialdict_file.write('%s: %s \n' % (key, term_dict[key]))

    specialdict_file.close()
    return term_dict


def make_inverted_index(term_dict):

    inverted_index = {} #(word, [(docID, occurenceWithinDocID), (docID, occurenceWithinDocID), ....] )
    stop_word_list = make_stop_word_list()

                                  #(term, docID)
    for keys, values in term_dict.items():
        #keys[0] is the term, keys[1] is docID, values is numOccurencesInDoc
        if keys[0] in inverted_index and keys[0] not in stop_word_list:
            inverted_index[keys[0]].append((keys[1], values))
        else:
            if keys[0] not in stop_word_list:
                inverted_index[keys[0]] = [(keys[1], values)]
            else:
                #print('didnt add ' + str(keys[0] + ' to inverted index b/c its a stop word'))
                continue
        if keys[0] not in stop_word_list:
            #sort the list of tuples that belong to the term by docID
            inverted_index[keys[0]] = sorted_nicely(inverted_index[keys[0]], itemgetter(0))

    inverted_index_file = open('inverted_index_file.txt', 'w+')

    for key in sorted(inverted_index):
        inverted_index_file.write('%s: %s \n' % (key, inverted_index[key]))
    inverted_index_file.close()
    print('# of unique words: ')
    print(len(inverted_index))
    return inverted_index

#inverted_index is a dictionary of {string: [ (string, int) ]
#inverted_index_with_tfidf is a dictionary of {string: [ (string, int, int) ]
def make_inverted_index_with_tf_idf(inverted_index):
    specialdict = pickle.load(open('specialdict.p', 'rb'))
    print('loaded bold dict from pickle')
    N = 1022 #Number of docs
    i = 0
    inverted_index_with_tfidf = {}

    for key, value in inverted_index.items():
        df_t = len(inverted_index[key]) #document freq: the # of docs that contain t
        idf = math.log10(N / df_t)
        for i in range(len(inverted_index[key])): #for each term, append tf.idf
            doc_number = inverted_index[key][i][0]
            tf_td = inverted_index[key][i][1]
            tf = math.log10(1 + inverted_index[key][i][1])
            tf_idf = tf * idf

            #*************if word is special, increase its tfidf ******************
            #specialdict holds (term,docId) as key
            tuplecheck = (key, inverted_index[key][i][0])
            if tuplecheck in specialdict:
                tf_idf *= 1.2  #need to play around w/ diff values
            #***********************************************************************

            if key in inverted_index_with_tfidf:
                inverted_index_with_tfidf[key].append( (doc_number, tf_td, tf_idf))
            else:
                inverted_index_with_tfidf[key] = [(doc_number, tf_td, tf_idf)]

    inverted_index_with_tfidf_file = open('inverted_index_with_tfidf_file.txt', 'w+')

    for key in sorted(inverted_index_with_tfidf):
        inverted_index_with_tfidf_file.write('%s: %s \n' % (key, inverted_index_with_tfidf[key]))
    inverted_index_with_tfidf_file.close()
    return inverted_index_with_tfidf