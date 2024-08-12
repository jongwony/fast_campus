import os
import sys
import json
import base64
import signal
from threading import Thread
from contextlib import contextmanager

import httpx
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from backend import sql_chain

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))
handler = SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN'))


def apply_slack_mrkdwn(markdown):
    return markdown.replace('**', '*')


@contextmanager
def loading(event):
    try:
        # Loading 이모지 추가
        app.client.reactions_add(
            channel=event["channel"],
            name="loading",
            timestamp=event['ts'],
        )
    finally:
        pass

    try:
        yield
    except Exception as e:
        raise e
    finally:
        try:
            app.client.reactions_remove(
                channel=event["channel"],
                name="loading",
                timestamp=event["ts"],
            )
        finally:
            pass


def sql_thread(event, say):
    with loading(event):
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

        say_response = say(text=':loading: 답변을 가져오고 있습니다...', thread_ts=thread_ts)
        gpt_iterator = sql_chain().stream({'question': text, 'history': context})
        gpt_response = ''
        for i, chunk in enumerate(gpt_iterator):
            gpt_response += chunk
            if gpt_response and i % 15 == 0:
                say_response = app.client.chat_update(
                    channel=say_response['channel'],
                    ts=say_response['ts'],
                    text=apply_slack_mrkdwn(gpt_response),
                )
        else:
            say_response = app.client.chat_update(
                channel=say_response['channel'],
                ts=say_response['ts'],
                text=apply_slack_mrkdwn(gpt_response),
            )


@app.event('app_mention')
def app_mention(event, say: Say):
    print(event)
    t = Thread(target=sql_thread, args=(event, say), daemon=False)
    t.start()


def at_terminate(signum, frame):
    print(signum, frame)
    # 실행 중인 스레드 종료
    print('소켓 핸들러 종료')
    try:
        # 블루 그린 배포를 진행할 경우 먼저 트래픽이 빠지기 때문에 핸들러 종료 과정이 필요 없다
        handler.close()
    except json.JSONDecodeError:
        pass
    sys.exit(128 + signum)


# Start your app
if __name__ == "__main__":
    # 시그널을 처리할 핸들러 등록
    signal.signal(signal.SIGTERM, at_terminate)
    signal.signal(signal.SIGINT, at_terminate)

    handler.start()
