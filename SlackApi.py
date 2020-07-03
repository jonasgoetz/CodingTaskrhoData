import csv
import json
import os
import urllib.request

from dotenv import load_dotenv


def json_request(method, token, channel, thread_ts):
    """"requesting a given method from the slack api and returning a
    dictionary
    """
    json_link = str("https://slack.com/api/conversations."
                    "{0:s}?token={1:s}&channel={2:s}{3:s}&pretty=1"
                    .format(method, token, channel, thread_ts))
    print("Requesting conversations.{0:s}".format(method), json_link)
    url_request = urllib.request.urlopen(json_link)
    data = url_request.read()
    encoding = url_request.info().get_content_charset('utf-8')
    json_data = json.loads(data.decode(encoding))
    return json_data


def get_all_channels():
    """retrieving all channels, saving channel id and name in a dict"""
    json_list = json_request("list", token, "", "")
    number_of_channels = len(json_list["channels"])
    channels_in_workspace = {}
    for i in range(number_of_channels):
        channel_name = json_list["channels"][i]["name"]
        channel_id = json_list["channels"][i]["id"]
        channels_in_workspace[channel_name] = channel_id
    return channels_in_workspace


def generate_csv_header():
    """writing only the header, replacing an old file if exists,
    returning a list
    """
    with open("Messages from Slack.csv", "w", newline="") as csvfile:
        csv_columns = [
            "type",
            "text",
            "user",
            "ts",
            "team",
            "thread_ts",
            "channelId",
            "is_child_message",
            "is_parent_message"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        return csv_columns


def dict_to_csv(dictionary, csv_columns):
    with open('Messages from Slack.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=csv_columns)
        writer.writerow(dictionary)


def retrieve_all_messages(csv_columns):
    """iterating through all messages of all channels and saving the
    values in the csv file
    """
    data_to_retrieve = (
        "type",
        "text",
        "user",
        "ts",
        "team",
        "thread_ts",
    )
    for key in channels_in_workspace:

        channel = channels_in_workspace[key]
        single_message = {}
        json_history = json_request("history", token, channel, "")
        l = (len(json_history["messages"]))
        for i in range(l):
            # iterating through keys of every message
            for key, value in json_history["messages"][i].items():
                if key in data_to_retrieve:
                    if key == "thread_ts":
                        # checks if a "thread_ts" exists
                        single_message["thread_ts"] = value
                        single_message["is_parent_message"] = True

                        # retrieving the replies
                        message_reply = {}
                        json_replies = json_request(
                            "replies", token, channel, "&ts=" + value)
                        l = (len(json_replies["messages"]))
                        # range starting from 1 to skip the first element
                        # because its the parent
                        for i in range(1, l):
                            for key, value in \
                                    json_replies["messages"][i].items():
                                if key in data_to_retrieve:
                                    message_reply[key] = value
                            message_reply["is_child_message"] = True
                            message_reply["channelId"] = channel
                            dict_to_csv(message_reply, csv_columns)
                    else:
                        single_message[key] = value
                        single_message["thread_ts"] = None
                        single_message["is_parent_message"] = None
            single_message["channelId"] = channel
            dict_to_csv(single_message, csv_columns)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("SLACK_API_TOKEN")
    get_all_channels()
    csv_columns = generate_csv_header()
    channels_in_workspace = get_all_channels()
    retrieve_all_messages(csv_columns)
