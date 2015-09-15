#!/usr/bin/python

import sys


# Event registry summary statistics

#imports
import numpy as np
import math
import json
from collections import Counter
import time
from eventregistry import * 
from datetime import date, datetime
print 'imports completed. Opening files...'

#files
with open("concept_articles.json", "r") as tfidf_file:
    tfidf = json.load(tfidf_file)
    tfidf_file.close()
    
#run = raw_input('Enter event ID (or blank to quit): ')
run = sys.argv[1]
startTime = datetime.now()
while run != '':
    file_number = int(np.floor((float(run)+1)/1000))
    print 'events-00' + '{0:03d}'.format(file_number) + '000.json'
    with open('events/events-00' + "{0:03d}".format(file_number) + '000.json') as data_file:
                    data = json.load(data_file)   
    the_event = data[str(run)]
#    print json.dumps(the_event, indent=4)
    print '\n'
    print 'Title: ' + the_event['info']['multiLingInfo']['eng']['title']
    print 'Date: ' + the_event['info']['eventDate']
    print 'Summary: ' + the_event['info']['multiLingInfo']['eng']['summary']
    print '\n'
    print 'Related Events:'
    for key, value in the_event['info']['multiLingInfo'].iteritems():
                if key == "eng":
                    summary = the_event['info']['multiLingInfo'][key]['summary'].split()
                    word_list = {}
                    word_count = 0
                    similarity_dict = {}
                    for word in summary:
                        word = word.replace(".", "")
                        word = word.replace(",", "")
                        word = word.replace("\"", "")
                        base_tfidf = tfidf[word][run]
                        for events in tfidf[word]:
                            try:
                                similarity_dict[events] = similarity_dict[events] + abs(base_tfidf - tfidf[word][events])
                            except:
                                similarity_dict[events] = abs(base_tfidf - tfidf[word][events])
                    similarity_list = sorted(similarity_dict.values(), reverse=True)
                    sorted_list = []
                    for value in similarity_dict:
                        if similarity_dict[value] > similarity_list[10]:
                            sorted_list.append([similarity_dict[value], value])
                            #print 'Event: ' + str(value) + ' with a score of ' + str(similarity_dict[value])
                    sorted_list = sorted(sorted_list, key=lambda x: x[0], reverse=True)
                    count = 0
                    while count < 10:
                        print str(count + 1) + '. Event: ' + str(sorted_list[count][1]) + ' with a score of ' + str(sorted_list[count][0])
                        count = count + 1
    print '\n'
    
#    er = EventRegistry(host = "http://eventregistry.org", logging = True)
#    q = QueryEvent(str(run));
#    q.addRequestedResult(RequestEventInfo())
#    q.addRequestedResult(RequestEventArticles(0, 10))        # get 10 articles about the event (any language is ok) that are closest to the center of the event
#    eventRes = er.execQuery(q);
#    print json.dumps(eventRes, indent=4)

    run = raw_input('Enter event ID (or blank to quit): ')


print 'This took ' + str(datetime.now() - startTime) + ' to run'
