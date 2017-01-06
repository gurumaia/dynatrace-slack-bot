#!/bin/bash
source bin/activate

export DYNATRACE_USER=YOURUSERNAME
export DYNATRACE_PASSWORD=YOURPASSWORD
export DYNATRACE_URL=https://YOURHOST:YOURPORT
export SLACK_BOT_TOKEN=YOURSLACKBOTTOKEN
export BOT_ID=YOURBOTID


nohup ./dynabot.py 2>&1 > dynabot.out &
