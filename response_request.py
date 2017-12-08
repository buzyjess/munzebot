# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 20:21:17 2017

@author: JeCelin
"""

import json
import os,sys
from flask import Flask,request,Response
import pprint
import time
import configparser
import requests
from pymessenger import Bot
import DataProcessing as dp
import BotDataPresentation as botdp
import ReadJson as rj
import matplotlib.pyplot as plot
import aws_interface as aws




#from apiai import ApiAI


#Config Parser 
def __init__(self):
    whitelist_domains =  ["https://s3-ap-southeast-2.amazonaws.com"]
    recepient_id = "1866057700072886"
    r=bot.add_whitelist_domains(recepient_id,whitelist_domains)
    print(r)
        

    


bot_config =configparser.ConfigParser()
bot_config.read('bot_config.ini')

ACCESS_KEY = bot_config['fb_page']['VERIFY_TOKEN']
PAGE_ACCESS_TOKEN= bot_config['fb_page']['PAGE_ACCESS_TOKEN']

bot =Bot(access_token ='EAAB2RDusw4YBACwITZBso5e0L719G9oVBvihvW2GtQTmzxhjCdHJViXoRMVIeC3G1fpUHh0TJyL1qE1MN58XCQZB61P5EWrls6CzfylLWsvQB4pLNrpEKVKTw39kBGZAKSVvDveij33uMaf1oMZBkGL1ncYz1ZCOIUp50ZAkmlyiAKpqiNUNe2')
                             
chat_intent = ['spend','exchange','income']
processing = 'processing...'
wrong_intent = "Chat bot couldnt decipher your question , Please ask again"
Debug = True
#log(ACCESS_KEY)


def log(printable):
    if Debug == True:
        print(printable)
        sys.stdout.flush()
    
def extract_message(message_payload):
    if 'message' in message_payload['entry'][0]['messaging'][0]:
        message = message_payload['entry'][0]['messaging']
    else:
        message = "No return message"
    return message 

def data_engine(nlp):
    message=""
    return message

def verify_message(message):
    if 'nlp' in message:
        nlp = message['nlp']
        if 'entities' in nlp:
            log( "for entities" )
            for intent in nlp['entities']:
                if True:
                    log( "if intent" + str(intent[0]['confidence']))
                    for intents in intents[0]:
                        log(type(intents))
                        intents = ""
                        log(type(intents))
                        log("before in confidence : " + str(nlp['entities']['intent'][0]['value']) + str((int(nlp['entities']['intent'][0]['confidence']))))
                        if (str(nlp['entities']['intent'][0]['value']) in chat_intent)  & \
                        (float(nlp['entities']['intent'][0]['confidence']) > .85):
                            message = data_engine(nlp)
                #            log("sucessful in confidence : " + str(nlp['entities']['intent'][0]['value']) + ":"+\
                #                str((float(nlp['entities']['intent'][0]['confidence']))))
                            return [True,processing]            
                        else:
                            #less confident repeat the question
                #            log("failed in confidence : " + str(nlp['entities']['intent'][0]['value']) + ":"+\
                #                str((float(nlp['entities']['intent'][0]['confidence']))))
                            return [True,wrong_intent]
                            
                        return [True,message['text']]
                return [False,wrong_intent]                
        return [False, wrong_intent]
    elif 'text' in message:
        log("text")
        return [False,wrong_intent]
    else:
        log("else")
        return [False,wrong_intent]
    
#def send_message(sender_id, message_text):
#    #log(str("message:" + str(message_text )))
#    elements_list = []
#    elements_list = [{
#            "title": "Classic T-Shirt Collection",
#            "subtitle": "See all our colors",
#            "image_url": "https://1103edf5.ngrok.io",          
#            "buttons": [
#              {
#                "title": "View",
#                "type": "web_url",
#                "url": "https://1103edf5.ngrok.io" ,
#                "messenger_extensions": True,
#                "webview_height_ratio": "tall",
#                "fallback_url": "https://1103edf5.ngrok.io"            
#              }]
#            },
#            {
#            "title": "Classic T-Shirt Collection",
#            "subtitle": "See all our colors",
#            "image_url": "https://1103edf5.ngrok.io",          
#            "buttons": [
#              {
#                "title": "View",
#                "type": "web_url",
#                "url": "https://1103edf5.ngrok.io",
#                "messenger_extensions": True,
#                "webview_height_ratio": "tall",
#                "fallback_url": "https://1103edf5.ngrok.io"            
#              }]
#		}
#	]
#    #message_text ="result"
#    #r = bot.send_text_message(sender_id,message)
#    r= bot.send_list_message(sender_id,elements_list)
#    log(r)
#    return r

#def send_message(sender_id,  image_url='https://s3-ap-southeast-2.amazonaws.com/mybot/localfile'):
#    """takes in user_id and a msg and sends it
#    takes in either a msg or image_url, not both"""
#    if image_url:
#        data = {'recipient': {'id': sender_id}, 
#                'message': {'attachment': 
#                {'type': 'image', 
#                'payload': {'url': image_url }}}}
#    log("send_message") 
#    post_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + 'EAAB2RDusw4YBACwITZBso5e0L719G9oVBvihvW2GtQTmzxhjCdHJViXoRMVIeC3G1fpUHh0TJyL1qE1MN58XCQZB61P5EWrls6CzfylLWsvQB4pLNrpEKVKTw39kBGZAKSVvDveij33uMaf1oMZBkGL1ncYz1ZCOIUp50ZAkmlyiAKpqiNUNe2'
#    resp = requests.post(post_url, json=data)
    

def send_message(sender_id,result_data,nlp_features,amount):
    category = nlp_features["category_value"]
    return_message = f"The amount you spend in  {category}  is AUD {amount:.2f}"
    log(return_message)
    r=bot.send_text_message(sender_id,message=return_message)
    log(r)
    return return_message


def send_file_message(sender_id,result_data,nlp_features):
    log("message in send_file")
    if result_data.empty:
        return
    result_data.plot.bar(x="category",y="amount")
    categories = nlp_features["category_value"]
    plot.title(f"Spend on {categories}")
    plot.xlabel("Dates"), plot.ylabel("Dollars")
    image_name = "13265489012341223412_Jeslin" + ".png"
    plot.savefig( image_name)
    access_key = aws.get_accesskey('munzebot')
    secret_access_key = aws.get_secret_accesskey('munzebot')
    bucket =aws.get_s3bucket('munzebot',access_key,secret_access_key)
    aws.upload_file_s3(bucket,image_name,image_name)
    time.sleep(1)
    file_url='https://s3-ap-southeast-2.amazonaws.com/munzebot/' + image_name
    #file_url='https://s3-ap-southeast-2.amazonaws.com/mybot/' +str(image_name)
    log(f"file_url {file_url}")
    r=bot.send_image_url(sender_id,file_url)
    log(r)
    return 

def send_greetings_message(sender_id,message):
    return_message = message

    r=bot.send_text_message(sender_id,message=return_message)
    log(r)
    return return_message
#        response_json={
#	"object": "text",
#	"entry": [{
#		"id": "1866057700072886",
#		"time": 1510978477914,
#		"messaging": [{
#				"message": {
#					"mid": "mid.$cAAb72AyWyUNl_psA-FfzVWmSz3sx",
#					"seq": 12,
#					"text": return_message
#
#				}
#			}
#
#		]
#	}]
#}
   

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def handle_verification():
    if (request.method =='POST'):
            message_payload =request.json
            #log("message_payload: " +str(message_payload))
            if message_payload['object'] == "page":
                for entry in message_payload['entry']:
                    for messages in entry['messaging']:
                        #log("messages :" + str(messages))
                        #return "ok" ,200
                        sender_id = messages['sender']['id']
                        recipient_id = messages['recipient']['id']
                        if 'message' in messages:
                            if 'nlp' in messages['message']:
                                log(  str( [{"sender_id":sender_id,"recepient_id":recipient_id}]))
                                nlp_features = botdp.extract_nlp_features(extract_message(message_payload))
                                if 'greetings_value' in nlp_features:
                                    send_greetings_message(sender_id,message="Hello")
                                elif "thanks_value" in  nlp_features:
                                    send_greetings_message(sender_id,message="Thanks Nice to Have you!!. Do you have any more queries?")
                                elif("category_conf" in nlp_features):
                                    df_grouped,datafile,amount =dp.intent_action(nlp_features,dp.temp_read_file())
                                    if df_grouped is not None:
                                        send_message(sender_id,df_grouped,nlp_features,amount)
                                        send_file_message(sender_id,df_grouped,nlp_features)
                                else:
                                    send_greetings_message(sender_id,"Munze bot couldnt interpret  your question")
                                
                #log(r.status_code)
            return "ok" ,200
    else:
        if (request.method == 'GET'):
            return request.args.get('hub.challenge' )
    
if __name__ =="__main__":
    print(time.localtime())
    app.run(debug=True,port = 80)

"""
@app.route('/data_test.csv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')
"""





#    
