# coding: utf-8

from resolvers.gitlab import trim_html_comment


sample_message = """# Hello World.
<!-- Test Comment -->
This is test message.
<!---->"""

def test_trim_html_comment():
    assert trim_html_comment(sample_message) ==  '# Hello World.\n\nThis is test message.\n'
