#!/usr/bin/env python3

import os
import sys
import slack



def main():
    scriptdir=os.path.dirname(os.path.realpath(__file__))
    with open(scriptdir+"/token.txt", 'r') as file:
        keyuser = file.readline().rstrip()
        keybot = file.readline().rstrip()

    # test sending
    client = slack.WebClient(token=keybot)
    response= client.chat_postMessage(channel='CAFBXMTMK',text="bots galore")
    assert response["ok"]
    assert response["message"]["text"] == "bots galore"
    print(response)

    # test reading
    client2 = slack.WebClient(token=keyuser)
    messages= client2.channels_history(channel='CAFBXMTMK')
    print(messages)
    print(type(messages))
if __name__ == '__main__':
    main()
