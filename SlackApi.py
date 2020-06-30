import os
import urllib.request
from pprint import pprint
import json
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("SLACK_API_TOKEN")


conversationList = "https://slack.com/api/conversations.list?" \
                   "token={0:s}&pretty=1".format(token)
urlList = urllib.request.urlopen(conversationList)
dataList = urlList.read()
encoding = urlList.info().get_content_charset('utf-8')
conversationListJson = json.loads(dataList.decode(encoding))
#pprint(conversationListJson)

numberChannels = len(conversationListJson["channels"])
channelsInWorkspace = {}
#generating Channel Id's
for i in range(numberChannels):
        channelName = conversationListJson["channels"][i]["name"]
        channelId = conversationListJson["channels"][i]["id"]
        channelsInWorkspace[channelName] = channelId

#going through one channel at a time
for key in channelsInWorkspace:
        channel = channelsInWorkspace[key]
        conversationHistory = str("https://slack.com/api/conversations."
                                  "history?token={0:s}&channel={1:s}&"
                                  "pretty=1&pretty=1".format(token, channel))
        urlHistory = urllib.request.urlopen(conversationHistory)
        dataHistory = urlHistory.read()
        encoding = urlHistory.info().get_content_charset('utf-8')
        conversationHistoryJson = json.loads(dataHistory.decode(encoding))
        #hier json in CSV speichern
        pprint(conversationHistoryJson)




