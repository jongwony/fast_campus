import os

from slack_bolt import App
from slack_bolt.context.say import Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from backend import onboard

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


def apply_slack_mrkdwn(markdown):
    return markdown.replace('**', '*')


@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "D079EE1RU12"
    user_id = event["user"]
    text = f"안녕하세요. <@{user_id}>! 🎉 이 채널에서 온보딩에 필요한 정보들을 물어보세요."
    say(text=text, channel=welcome_channel_id)


def is_im_message(event):
    return event.get("channel_type", "") == "im"


@app.event(event={
    "type": "message",
    "subtype": None,
}, matchers=[is_im_message])
def message_im_event(event, say: Say):
    print(event)
    gpt_response = onboard().invoke(event['text'])
    say(apply_slack_mrkdwn(gpt_response), mrkdwn=True)


@app.event(event={
    "type": "message",
    "subtype": "message_changed",
}, matchers=[is_im_message])
def message_im_change_event(event, say: Say):
    print(event)
    gpt_response = onboard().invoke(event['message']['text'])
    say(apply_slack_mrkdwn(gpt_response), mrkdwn=True)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()
