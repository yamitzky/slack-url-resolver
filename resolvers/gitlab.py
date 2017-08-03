import os
import re
import urllib.parse

import requests

from . import skip_bot_message


@skip_bot_message
def resolve(client, event):
    GITLAB_DOMAIN = os.environ['GITLAB_DOMAIN']
    ids = re.findall(f'{GITLAB_DOMAIN}/(.+)/(issues|merge_requests)/(\d+)', event['text'])
    for project, issue_type, issue_id in ids:
        project = urllib.parse.quote_plus(project)
        issue = requests.get(
            f'{GITLAB_DOMAIN}/api/v4/projects/{project}/{issue_type}/{issue_id}',
            headers={'PRIVATE-TOKEN': os.environ['GITLAB_TOKEN']}
        ).json()
        client.api_call(
            'chat.postMessage',
            channel=event['channel'],
            attachments=[{
                'color': '#eb763d',
                'title': issue['title'],
                'title_link': issue['web_url'],
                'text': issue['description'],
                'author_name': issue['author']['name'],
                'author_icon': issue['author'].get('avatar_url'),
                'author_link': issue['author']['web_url'],
            }]
        )
