import os
import base64

import httpx
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from backend import sql_chain

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


def apply_slack_mrkdwn(markdown):
    return markdown.replace('**', '*')


@app.event('app_mention')
def app_mention(event, say: Say):
    print(event)

    thread_ts = event.get("thread_ts") or event["ts"]
    text = event["text"]
    conversations = app.client.conversations_replies(
        channel=event['channel'],
        ts=thread_ts,
    )

    context = [
        ('ai' if msg['user'] == 'U0795AUR6NA' else 'human', msg['text'])
        for msg in conversations.data['messages']
    ][:-1]

    # 마지막 대화의 이미지
    for file in event.get('files', []):
        image_url = file['url_private_download']
        headers = {'Authorization': f'Bearer {os.getenv("SLACK_BOT_TOKEN")}'}
        response = httpx.get(image_url, headers=headers)
        image_data = base64.b64encode(response.content).decode()
        image_content = {
            'type': 'image_url',
            'image_url': {'url': f'data:{file["mimetype"]};base64,{image_data}'}
        }
        context.append(('human', [image_content]))

    gpt_response = sql_chain().invoke({'question': text, 'history': context})
    say(text=apply_slack_mrkdwn(gpt_response), thread_ts=thread_ts)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()
