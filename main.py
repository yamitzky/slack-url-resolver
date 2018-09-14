import importlib
from logging import getLogger
import os
import time
import threading

from slackclient import SlackClient


logger = getLogger(__name__)


def wrap_resolver(resolver):
    def wrapper(client, event):
        def post_message(**message):
            payload = {k: v for k, v in message.items()}
            if 'thread_ts' not in message and 'thread_ts' in event:
                payload['thread_ts'] = event['thread_ts']
            if payload.get('file') or payload.get('content'):
                if 'channels' not in message:
                    payload['channels'] = [event['channel']]
                client.api_call(
                    'files.upload',
                    **payload
                )
            else:
                if 'channel' not in message:
                    payload['channel'] = event['channel']
                client.api_call(
                    'chat.postMessage',
                    **payload
                )

        try:
            resolver.resolve(post_message, event)
        except Exception as e:
            logger.exception(e)
            client.rtm_send_message(event['channel'], str(e))
    return wrapper


def main():
    if 'RESOLVERS' in os.environ:
        resolvers = os.environ['RESOLVERS'].split(',')
    else:
        resolvers = ['resolvers.twitter', 'resolvers.qiita', 'resolvers.gitlab']
    resolvers = [wrap_resolver(importlib.import_module(r)) for r in resolvers]

    client = SlackClient(os.environ['SLACK_BOT_TOKEN'])
    logger.info('Connecting...')
    client.rtm_connect()
    while True:
        try:
            for event in client.rtm_read():
                logger.error(event)
                if event.get('type') == 'message' and event.get('text'):
                    for resolver in resolvers:
                        threading.Thread(target=resolver, args=(client, event)).start()
        except Exception as e:
            logger.exception(e)
            time.sleep(10)
        time.sleep(1)


if __name__ == '__main__':
    main()
