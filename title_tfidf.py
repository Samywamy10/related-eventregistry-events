# Event registry summary statistics

#imports
import numpy as np
import math
import json
from collections import Counter
import time
from eventregistry import * 
from datetime import date, datetime
print 'imports completed'

startTime = datetime.now()
file_counter = 876 #all files
#file_counter = 10 #realistic
total_files = file_counter * 1000
files = 0 #file incrementer
event = 0 #event within file incrementer
output = []
concept_main_list = {}
max_sum = 0
def hashing(word):
    sum = 0
    global max_sum
    for pos in range(len(word)):
        sum = sum + ord(word[pos]) * (pos + 1)
        if (sum > max_sum):
            max_sum = sum
    
    return sum%2000000

def list_check(list,index):
    try:
        return list[index]
    except IndexError:
        return 0

#count = 0
#while count < 2000000: #initialise the hash table
#    concept_main_list.append(0)
#    count = count + 1

with open("title_idf.json", "r") as idf_file:
    idf = json.load(idf_file)
    idf_file.close()
    
while files < file_counter:
    concept_list = []
    print 'events-00' + '{0:03d}'.format(files) + '000.json'
    print datetime.now() - startTime
    print str(round(float(files) / float(file_counter),4) * 100) + '%'
    with open('events/events-00' + "{0:03d}".format(files) + '000.json') as data_file:
            data = json.load(data_file)        
    #loop through events in json file
    count = len(data) + (files * 1000)
    while event < count:
        event_dict = {}
        print event
        the_event = data[str(event)] #the_event refers to one event
        if 'info' in the_event: #if the event isn't a merge with another event
            the_event = the_event['info']
        if 'uri' in the_event:
            event_dict['ID'] = the_event['uri']
        if 'stories' in the_event:
            #event_dict['story_title'] = the_event['stories'][0]['title']
            #event_dict['story_lang'] = the_event['stories'][0]['lang']
            #event_dict['story_summary'] = the_event['stories'][0]['summary']
            #event_dict['story_date'] = the_event['stories'][0]['averageDate']
            var0 = 0        
        if 'concepts' in the_event:
            #concept_number = 0
            #concept_list = []
            #for concept in the_event['concepts']:
                #the_hash = hashing(concept['labelEng']) 
                #print the_hash
                #concept_main_list[the_hash] = concept_main_list[the_hash] + 1
                #concept_main_list.insert(the_hash,initial_count + 1)
                #event_dict['concept' + str(concept_number)] = concept['labelEng']
                #concept_list.append(concept['labelEng'])
                #concept_number = concept_number + 1
            event_dict['concepts'] = concept_list
        if 'eventDate' in the_event:
            if the_event['eventDate'] != "":
                event_date = datetime.strptime(the_event['eventDate'], "%Y-%m-%d").date()       
                event_dict['event_date'] = the_event['eventDate']                            
        if 'multiLingInfo' in the_event:
            for key, value in the_event['multiLingInfo'].iteritems():
                if key == "eng":
                    summary = the_event['multiLingInfo'][key]['title'].split()
                    word_list = {}
                    word_count = 0
                    for word in summary:
                        word = word.replace(".", "")
                        word = word.replace(",", "")
                        word = word.replace("\"", "")
                        if word_list.has_key(word):
                            word_list[word] = word_list[word] + 1
                        else:
                            word_list[word] = 1
                        word_count = count + 1         
                    for word in word_list:
                        #the_hash = hashing(word)
                        print word
                        print word_list[word]
                        if concept_main_list.has_key(word):
                            concept_main_list[word][event_dict['ID']] = idf[word] * float(word_list[word]) / float(word_count)
                        else:
                            concept_main_list[word] = {}
                            concept_main_list[word][event_dict['ID']] = idf[word] * float(word_list[word]) / float(word_count)
                    
                
            the_event = the_event['multiLingInfo'].values()
            #print the_event[0]['title']
        #" + str("{0:03d}".format(int(round(math.ceil(event / 1000) * 1000,4)))) + "
        output.append(event_dict)
        #with open("flatten.json", "a") as myfile:
        #    myfile.write(json.dumps(event_dict, indent=4))
        event = event + 1;
    files = files + 1 #increment the file counter
startTime = datetime.now()

#print concept_main_list

with open("title_tfidf.json", "w") as myfile:
    myfile.write(json.dumps(concept_main_list, indent=0))
    myfile.close()

print 'There are ' + str(event) + ' events.'
#print json.dumps(output, indent=4)


print 'This took ' + str(datetime.now() - startTime) + ' to run'
