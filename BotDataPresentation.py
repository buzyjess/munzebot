# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:53:58 2017

@author: JeCelin
"""

import numpy as np
import pandas as pd
import os
import shutil 
from pandas import DataFrame 
import re
import configparser
import requests 
import csv   
import time
import pprint as pp
import sys

import ReadJson as rj
 
Debug = True


def log(printable):
    'Utility to print the data'
    if Debug == True:
        print(printable,file=sys.stdout)
        sys.stdout.flush()

#json_file = "nlp5.json"
#json_dir = "C:/Users/Celin/.ssh/messengerbot/botenv/Scripts"
#file = os.path.join(json_dir,json_file)


#def bot_read_csv(filename, fildir =  None,source ='local'):
#    'Fuction to read the users data from local or cloud' 
#    if source == 'local':
#        if fildir is None:
#            datafile = pd.read_csv(filename)  
#        else:
#            datafile = pd.read_csv(os.path.join(fildir,filename))
#    return datafile
#
#datafile = bot_read_csv(filename="Source_data.csv",fildir = "C:/Users/Celin/.ssh/messengerbot/botenv/Scripts",source='local'  )

#json_data = rj.read_json(file)
#
#message = json_data['entry'][0]['messaging']
#
#print(message[0]['sender']['id'] )
#pp.pprint(message)

def extract_nlp_features(message):
    'Extract the differrent features/entities of the nlp intent and returns a simple dictionary of what is needed'
    #log("In extract_nlp_features" + str(message))
    nlp_features = {}
    nlp={}
    nlp_features["senderid"] =message[0]['sender']['id'] 
    nlp_features["recepientid"] = message[0]['recipient']['id']
    nlp_features["message_text"] = message[0]['message']['text']
    nlp = message[0]['message']['nlp']
    if "greetings" in  nlp['entities']:
        nlp_features["greetings_value"] = message[0]['message']['text']
        return(nlp_features)
    if "thanks" in  nlp['entities']:
        nlp_features["thanks_value"] = message[0]['message']['text']
        return(nlp_features)
    nlp_features["intent_conf"] = nlp['entities']['intent'][0]["confidence"]
    nlp_features["intent_value"] = nlp['entities']['intent'][0]["value"]
    if "duration" in nlp['entities']:
        nlp_features["period"]["duration_conf"] = nlp['entities']['duration'][0]["confidence"]
        nlp_features["duration_value"] = nlp['entities']['duration'][0]["value"]
        nlp_features["duration_unit"] = nlp['entities']['duration'][0]["unit"]
    elif "datetime" in nlp['entities']:
            if "type" in nlp['entities']['datetime'][0]:
                if nlp['entities']['datetime'][0]["type"] == "value" :
                    nlp_features["datetime_conf"] = nlp['entities']['datetime'][0]["confidence"]
                    nlp_features["datetime_from"] = nlp['entities']['datetime'][0]["value"]
                    nlp_features["datetime_to"] = ""
                    
                elif nlp['entities']['datetime'][0]["type"] == "interval" :
                        nlp_features["datetime_conf"] = nlp['entities']['datetime'][0]["confidence"]
                        nlp_features["datetime_from"] = nlp['entities']['datetime'][0]["from"]["value"]
                        nlp_features["datetime_to"] = nlp['entities']['datetime'][0]["to"]["value"]
    #if ("datetime_conf" & "intent_conf"  &  "category_conf" in nlp_features.keys()):
    #return                 
    nlp_features["category_conf"] = nlp['entities']['category'][0]["confidence"]
    nlp_features["category_value"] = nlp['entities']['category'][0]["value"]
    #nlp_features["category_conf"] = nlp['entities']
    #pp.pprint(nlp_features)
    return(nlp_features)      
    

def validate_fb_message(message_payload):
     if message_payload['object'] == "page":
         log("In page")
         if "entry" in message_payload:
             log("In enrty")
             for entry in message_payload['entry']:
                 if 'messaging' in entry:
                     messaging = entry['messaging']
                     log("In messaging")
                     if 'message' in messaging[0]:
                         log("In message")
                         message = messaging[0]['message']
                         if 'nlp' in message:
                             log("In NLP")
                             nlp = message['nlp']
                             if 'entities' in nlp:
                                 log('In Entiies')
                                 entities = nlp['entities']
                                 missing_nlp_entities = set(['category','duration','intent'])-entities.keys()
                                 existing_entities = set(['category','duration','intent']) -missing_nlp_entities
                                 for entity in existing_entities:
                                     log(entity)
                                     log(entities[entity][0])
                                     if  all( keys in ['confidence' , 'value'] for keys in entities[entity][0]):
                                         log("In confidence and value")
                                     else:
                                         return [False,"No confidence"]
                                 else:
                                     return[False,'No Category']
                             else:
                                 return[False,'No Entities']
                         else:
                             [False,"No NLP"]
                    
                     else:
                         return [False ,"No message"]
                 else:
                     return [False, "No messaging"]
         else:
                 return [False, "Entry missing in Payload"]
     else:
             return [False,"Page not found"]
             #for entry in message_payload['entry']:
#    
#                    for messages in entry['messaging']:
#                        sender_id = messages['sender']['id']
#                        recipient_id = messages['recipient']['id']
#                        #printable = [{"sender_id":sender_id,"recepient_id":recipient_id}]
#                        return_message = verify_message(extract_message(message_payload))
             
log("Loaded BotDataPresentation")

#log(validate_fb_message(json_data))
    
    
#





#pp.pprint(extract_nlp_features(message))
#    
