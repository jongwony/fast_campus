import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from backend import lol_chain

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
    thread_ts = event["thread_ts"] or event["ts"]
    text = event["text"]
    conversations = app.client.conversations_replies(channel=event['channel'], ts=thread_ts)
    context = [
        ('ai' if msg['user'] == 'U0795AUR6NA' else 'human', msg['text'])
        for msg in conversations.data['messages']
    ][:-1]
    response = lol_chain(text, context)
    say(text=response, thread_ts=thread_ts)





# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
