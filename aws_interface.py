# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:39:24 2017

@author: JeCelin
"""


import boto3 as aws
import configparser



bot_config =configparser.ConfigParser()
bot_config.read('bot_config.ini')   

def __init__(self):
    self.bot_config =configparser.ConfigParser()
    bot_config.read('bot_config.ini')   

    


def get_accesskey(bucket=None):
    'Return the access key for the <bucket>'
    if bucket is not None:    
        return bot_config['aws']['ACCESS_KEY']
    else:
        return "No Keys" 
    

def get_secret_accesskey(bucket=None):
    'Return the secret access key for the <bucket>'
    if bucket is not None:    
        return bot_config['aws']['SECRET_ACCESS_KEY']
    else:
        return "No Keys" 
    


def get_s3bucket(bucketname,accesskey,secretacesskey):
    'Return the an instance of the '
    s3 = aws.resource('s3', 
                    aws_access_key_id=accesskey, 
                    aws_secret_access_key=secretacesskey)
    
    bucket = s3.Bucket(bucketname)
        
    return bucket
    
def upload_file_s3(bucket,absfile,key):
    'Upload file to <bucket> '
    #bucket.upload_file('file.html','botresult/{}'.format('file_2'))
    bucket.upload_file(absfile,key,ExtraArgs={'ACL':'public-read-write','ContentType':'image/png'})
    #bucket.put_object(Key=key, Body=absfile,ContentType="image/png", ACL="public-read")
 
def download_file_s3(bucket,absfile,key):
    'Upload file to <bucket> '
    #bucket.upload_file('file.html','botresult/{}'.format('file_2'))
    bucket.download_file(absfile,key) 
        
        
    
     

  
    
