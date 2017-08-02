import functools


def skip_bot_message(func):
    @functools.wraps(func)
    def wrapper(client, event):
        if event.get('subtype') == 'bot_message':
            return
        return func(client, event)
    return wrapper
