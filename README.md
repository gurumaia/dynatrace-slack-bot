# What is it?
This is a Slack bot written in Python to talk to you Dynatrace dashboards via the Dynatrace REST API.

# How to use it
1. Create a dashboards.py file in the root (check the examples dir)
2. Set the required environment variables (check start.sh in the examples dir for an idea):
  * DYNATRACE_USER
  * DYNATRACE_PASSWORD
  * DYNATRACE_URL
  * SLACK_BOT_TOKEN
  * BOT_ID
3. Create a python virtualenv: `virtual .`
4. Switch to your virtualenv: `source bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

# Borrowed stuff
The code here leans heavily on [this post on fullstackpython](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) including some shameless copy/paste.
