import importlib
from logging import getLogger
import os
import time
import threading

from slackclient import SlackClient


logger = getLogger(__name__)


def main():
    if 'RESOLVERS' in os.environ:
        resolvers = os.environ['RESOLVERS'].split(',')
    else:
        resolvers = ['resolvers.twitter', 'resolvers.qiita', 'resolvers.gitlab']
    resolvers = [importlib.import_module(r) for r in resolvers]

    client = SlackClient(os.environ['SLACK_BOT_TOKEN'])
    logger.info('Connecting...')
    client.rtm_connect()
    while True:
        try:
            for event in client.rtm_read():
                logger.debug(event)
                if event.get('type') == 'message' and event.get('text'):
                    try:
                        for resolver in resolvers:
                            threading.Thread(target=resolver.resolve, args=(client, event)).start()
                    except Exception as e:
                        logger.exception(e)
                        client.rtm_send_message(event['channel'], str(e))
        except Exception as e:
            logger.exception(e)
            time.sleep(10)
        time.sleep(1)


if __name__ == '__main__':
    main()
