import os
import re

import requests

from . import skip_bot_message


@skip_bot_message
def resolve(post_message, event):
    QIITA_DOMAIN = os.environ['QIITA_DOMAIN']
    ids = re.findall(f'{QIITA_DOMAIN}/.+/items/([0-9a-zA-Z]+)', event['text'])
    for item_id in ids:
        item = requests.get(
            f'{QIITA_DOMAIN}/api/v2/items/{item_id}',
            headers={'Authorization': f'Bearer {os.environ["QIITA_TOKEN"]}'}).json()
        post_message(
            attachments=[{
                'color': '#79b74a',
                'title': item['title'],
                'title_link': item['url'],
                'text': item['body'],
                'author_name': item['user']['name'],
                'author_icon': item['user']['profile_image_url'],
                'author_link': item['user'].get('website_url'),
            }]
        )
