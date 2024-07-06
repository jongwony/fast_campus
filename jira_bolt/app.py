import os

import jmespath
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.context.say import Say
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.event("reaction_added")
def jira_create(event, say: Say):
    # 유저 리스트 가져오기
    slack_users_list = app.client.users_list()
    slack_users_map = {
        x['id']: {
            'real_name': x['real_name'],
            'email': jmespath.search('profile.email', x)
        }
        for x in slack_users_list.data['members']
        if x['deleted'] is False
    }

    conversations = app.client.conversations_replies(
        channel=event['item']['channel'],
        ts=event['item']['ts'],
    )

    conversations_str = ''
    for msg in conversations.data['messages']:
        user_name = slack_users_map[msg['user']]['real_name']
        refined_text = f'{user_name}: """{msg['text']}"""\n'
        conversations_str += refined_text
        
    print(conversations_str)

    assignee = slack_users_map[event['user']]                          # 이모지를 다는 사람(담당자) 이름 가져오기
    reporter = slack_users_map[event['item_user']]                     # 이모지가 달린 사람(보고자) 이름 가져오기
    print(reporter, assignee)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()
