import os
import re
import urllib.parse

import requests

from . import skip_bot_message


GITLAB_DOMAIN = os.environ['GITLAB_DOMAIN']
GITLAB_ID_PATTERN = re.compile(f'{GITLAB_DOMAIN}/(.+)/(issues|merge_requests)/(\d+)')
COMMENT_PATTERN = re.compile(r'''<!--.*?-->''', re.MULTILINE | re.DOTALL)


@skip_bot_message
def resolve(post_message, event):
    ids = GITLAB_ID_PATTERN.findall(event['text'])
    for project, issue_type, issue_id in ids:
        project_id = urllib.parse.quote_plus(project)
        issue = requests.get(
            f'{GITLAB_DOMAIN}/api/v4/projects/{project_id}/{issue_type}/{issue_id}',
            headers={'PRIVATE-TOKEN': os.environ['GITLAB_TOKEN']}
        ).json()
        post_message(
            attachments=[{
                'color': '#eb763d',
                'title': f"[{project}]{issue['title']}",
                'title_link': issue['web_url'],
                'text': trim_html_comment(issue['description']),
                'author_name': issue['author']['name'],
                'author_icon': issue['author'].get('avatar_url'),
                'author_link': issue['author']['web_url'],
            }]
        )

def trim_html_comment(html):
    return COMMENT_PATTERN.sub('', html)
    
