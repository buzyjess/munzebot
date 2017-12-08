# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:53:05 2017

@author: JeCelin
"""



import os
from pandas import DataFrame as df
import pprint
import sys
import ReadJson as rj
import pandas as pd
from dateutil.relativedelta import *
import BotDataPresentation as bdt
import datetime
Debug = True

#json_file = "nlp3.json"
#json_dir = "C:/Users/Celin/.ssh/messengerbot/botenv/Scripts"
#file = os.path.join(json_dir,json_file)
#
#json_data = rj.read_json(file)
#
#
#
#nlp_features = bdt.extract_nlp_features(message)


def __init__():
    nlp_featues = {}
    
#    datafile = pd.DataFrame()
#    json_file = "nlp2.json"
#    json_dir = "C:/Users/Celin/.ssh/messengerbot/botenv/Scripts"
#    file = os.path.join(json_dir,json_file)
#    json_data = rj.read_json(file)
#    message = json_data['entry'][0]['messaging']

    
def log(printable):
    'Utility to print the data'
    if Debug == True:
        print(printable,file=sys.stdout)
        sys.stdout.flush()

def action_spend(nlp_features=None,datafile=None):
    log("In Action Spend")
#    period_convert = {"day": "days", "week": "weeks", "month":"months", "year":"years"}
#    unit = -nlp_features['duration_value']
#    frequency = period_convert[nlp_features['duration_unit']]
#    kw = {frequency:unit}
#    log("In kw:"+ str(kw))
#    end_datetime = pd.to_datetime(datetime.datetime.now())
#    start_datetime= end_datetime +relativedelta(**kw )
    if "datetime_from" not in nlp_features:
        start_datetime=pd.to_datetime(datetime.datetime.now() -relativedelta(years =1))
    else:
        if (nlp_features["datetime_from"] in [ None,'']) : 
            start_datetime=pd.to_datetime(datetime.datetime.now() -relativedelta(years =1))
        else:
            start_datetime=nlp_features["datetime_from"]
    if "datetime_to" not in nlp_features:
        end_datetime=pd.to_datetime(datetime.datetime.now())
    else:
        if (nlp_features["datetime_to"] in [ None,'']) : 
            end_datetime=pd.to_datetime(datetime.datetime.now())
        else:
            end_datetime=nlp_features["datetime_to"]
#
    if nlp_features['category_value'] is None:
        datafile1=datafile
    else:
        datafile1 = datafile[datafile.category.str.startswith(str.strip(str.lower(nlp_features['category_value'])),na= False)         ].copy()
        
    log("start_time: " +str(start_datetime) + " endtime: " + str(end_datetime))
    date_filter = (datafile1.date > start_datetime)  & (datafile1.date < end_datetime) 
    datafile1 = datafile1[date_filter].copy()
    df_grouped =datafile1.groupby('category',as_index= False)['amount'].sum()
    if  df_grouped.shape[0] == 1 : 
        amount = df_grouped.iloc[0,1]
    else:
        amount =df_grouped['amount'].sum()
    #amount = amount.abs()
    log(df_grouped)
    return df_grouped,datafile1,abs(amount)   
        

# read file and parse it based on the source. 

def bot_read_csv(filename, fildir =  None,source ='local'):
    'Fuction to read the users data from local or cloud' 
    if source == 'local':
        if fildir is None:
            datafile = pd.read_csv(filename)  
        else:
            datafile = pd.read_csv(os.path.join(fildir,filename))
    elif source == 'S3':
        bot_read_s3_csv(filename,filedir,parase_dates = 'date')
    else:
        return "File not found"
    datafile.category =datafile.category.str.lower()
    datafile.date = pd.to_datetime(datafile['date'],dayfirst = True)
    log("Exiting bot_read_csv")
    return datafile


def intent_action(nlp_features=None,datafile=None):
    #log("In intent_action" + str(datafile.columns ))
    #log(nlp_features)
    intent= nlp_features['intent_value']
    if intent == "spend":
      df_grouped,datafile1,amount = action_spend(nlp_features,datafile)
    elif intent == "income":
       action_income(nlp_features,datafile)
    elif intent == "savings":
        action_savings(nlp_features,datafile)
    else:
        pass
    return df_grouped,datafile1,amount 


def temp_read_file():
    datafile = bot_read_csv(filename="Source_data.csv",fildir = "C:/Users/Celin/.ssh/botenv/Scripts",source='local'  )
    return datafile
    
#Read datafile either the S3 or local source"
#extract nlp features for the messafe

#call the correct intent action
#datafile=temp_read_file()
#intent_action(nlp_features=nlp_features,datafile=datafile)

    

    
