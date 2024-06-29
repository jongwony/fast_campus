import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from backend import lol_chain

from openai import APIError


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("안녕")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    message_text = message["text"]
    response = lol_chain(message_text)
    say(response, thread_ts=message["ts"])


# When a user joins the workspace, send a message in a predefined channel asking them to introduce themselves
@app.event("app_mention")
def lol_player(event, say):
    thread_ts = event.get("thread_ts") or event["ts"]
    text = event["text"] * 100000
    conversations = app.client.conversations_replies(channel=event['channel'], ts=thread_ts)
    context = [
        ('ai' if msg['user'] == 'U0795AUR6NA' else 'human', msg['text'])
        for msg in conversations.data['messages']
    ][:-1]

    try:
        response = lol_chain(text, context)
    except APIError as e:
        response = f"API error: {e}"
        return say(blocks=error_template(e)['blocks'], thread_ts=thread_ts)

    say(text=response, thread_ts=thread_ts)


def error_template(error: APIError):
    notification_template = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "An error occurred in the API:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error Message:*\n{error.message}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Status Code:* {error.status_code}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Request ID:* {error.request_id if error.request_id else 'N/A'}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error Code:* {error.code if error.code else 'None'}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "For more details, please check the logs or contact support."
                    }
                ]
            }
        ]
    }
    return notification_template


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
