#!/usr/bin/env python3

# simple reservation tool. People can reserve/volunteer for specific days in the week
# via social channels, at the moment slack.
# This information can then be posted somewhere, at the moment slack and docuwiki

import os
import sys
import slack
import getopt
import json
import re

# Important constants
CHANNEL='CAFBXMTMK'

weekdays=['montag','dienstag','mittwoch','donnerstag','freitag','samstag','sonntag']

def slackRead(key):
    filter=re.compile(r'(?i)(?:ich\s+)?kann\s+(?:am\s+)?([a-z]+)')
    days={}
    for d in weekdays:
        days[d]=1
    
    client = slack.WebClient(token=key)
    history= client.channels_history(channel='CAFBXMTMK')
    for message in history.get("messages"):
        if message['type']=="message":
            result= filter.match(message['text'])
            if result:
                weekday=str.lower(result.group(1))
                print(message['user'],'kann',weekday)
                if weekday in days:
                    del days[weekday]
                else:
                    weekday='<'+weekday+'>'
                    print(weekday,'nicht gefunden')
    return(days)
            
        

    
def slackWrite(key,message):
    client = slack.WebClient(token=key)
    response= client.chat_postMessage(channel='CAFBXMTMK',text=message)
    assert response["ok"]

    
def docuWikiWrite(message):
    a=1

def main(argv):
    
    try:
        opts, optargs = getopt.getopt(argv, "h?", ["silent"])

    except getopt.ParameterError:
        sys.exit(2)

    silent=False;
    for opt, arg in opts:
        if opt in ("--silent"):
            silent=True;
        if opt in ("-?","-h"):
            print("labsitterbot   [-h] [-?] [--silent]\n"
                  "-h,-?      this help"
                  "--silent   post no message to slack")
            sys.exit(0);

    try:
        scriptdir=os.path.dirname(os.path.realpath(__file__))
        with open(scriptdir+"/token.txt", 'r') as file:
            keyuser = file.readline().rstrip()
            keybot = file.readline().rstrip()
        if len(keyuser)<5 or len(keybot)<5:
            print("\nERROR getting slack keys\n")
    except (OSError,NameError):
        print("\nERROR loading slack keys\n")
        sys.exit(3)
        
    days= slackRead(keyuser)
    m=""
    for weekday in weekdays:
        if weekday in days:
            m= m+' '+weekday
    message='Noch niemand gemeldet für: '+m
    print(message)
    if not silent:
        slackWrite(keybot,message)
    docuWikiWrite(message)

 
if __name__ == '__main__':
    main(sys.argv[1:])
