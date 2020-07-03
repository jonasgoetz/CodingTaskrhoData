# Coding Task rho Data
	
### General
This script is designed to retrieve messages from a slack workspace.
Those messages are then being saved into one single CSV file.
#
### Technologies
The project uses the following technologies: 
* Slack Conversations API
* Python 3.7.6
#
### Slack Conversations API
#### Used Methods:
 * conversations.list <br/> https://api.slack.com/methods/conversations.list
 * conversations.history <br/> https://api.slack.com/methods/conversations.history
 * conversations.reply <br/> https://api.slack.com/methods/conversations.reply

#### Required Scopes:
 * channels:history
 * channels:read
 * groups:history
 * groups:read
 * mpim:history
 * mpim:read
 * im:history
 * im:read 
 
#
### Setup
 * Create a new Slack API App <br/> https://api.slack.com/
 * Navigate to "OAuth & Permissions"
    *  Add all the scopes described above for both Bot and User
    *  Click on "Install to Workspace"
    *  Copy "OAuth Access Token"
 * Set up a .env file with the following content:
 ```
SLACK_API_TOKEN=xxx-your-token-here
```
* Install the necessary dependencies:
 ```
$ pip install -r requirements.txt
```
#
### Usage
After setting up everything successful you can run the Python script.
#
### Messages from Slack.csv
* Each time you run the Script the csv file is being overwritten
* User, Channel or Team parameters are their Ids
* "thread_ts" indicates a thread, so a message either has replies or is a reply 
* "thread_ts" is the unique id that describes the time when the first response was posted
* If a message has replies the parameter "is_parent_message" is set to "True"
* If a message is a reply to another message the parameter "is_child_message" is set to "True"
* parent and child messages with the same "thread_ts" are related


