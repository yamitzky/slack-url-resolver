import os
import re

import tweepy


def resolve(post_message, event):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    ids = re.findall('https?://[^/]*twitter.com/([a-zA-Z0-9_]+)(?:/status/(\d+))', event['text'])

    for screen_name, status_id in ids:
        status = api.get_status(id=status_id, tweet_mode='extended')
        attachments = [{
            'color': '#55acee',
            'text': status.full_text,
            'author_name': f'{status.user.name} @{status.user.screen_name}',
            'author_link': f'https://twitter.com/{status.user.screen_name}',
            'author_icon': f'https://twitter.com/{status.user.screen_name}/profile_image',
        }]
        for media in status.extended_entities.get('media', []):
            attachments.append({
                'color': '#55acee',
                'title': media['media_url_https'],
                'image_url': media['media_url_https'],
            })
        post_message(attachments=attachments)
