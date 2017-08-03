import os
import re

import tweepy

from . import skip_bot_message


@skip_bot_message
def resolve(client, event):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    ids = re.findall('https?://[^/]*twitter.com/([a-zA-Z0-9_]+)(?:/status/(\d+))', event['text'])

    for screen_name, status_id in ids:
        status = api.get_status(id=status_id)
        attachment = {
            'color': '#55acee',
            'text': status.text,
            'author_name': f'{status.user.name} @{status.user.screen_name}',
            'author_link': f'https://twitter.com/{status.user.screen_name}',
            'author_icon': f'https://twitter.com/{status.user.screen_name}/profile_image',
        }
        if status.entities.get('media'):
            attachment['image_url'] = status.entities['media'][0]['media_url_https']
        client.api_call(
            'chat.postMessage',
            channel=event['channel'],
            attachments=[attachment]
        )
