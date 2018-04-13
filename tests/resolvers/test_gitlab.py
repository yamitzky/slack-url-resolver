# coding: utf-8

from resolvers.gitlab import trim_html_comment


SAMPLE_HTML = '''# The Zen of Python
Beautiful is better than ugly.
<!-- comment --><!-- comment -->
Explicit is better than implicit.
<!--
  Multi line comment
-->
Simple is better than complex.
<!---->
...'''

EXPECTED_HTML = '''# The Zen of Python
Beautiful is better than ugly.

Explicit is better than implicit.

Simple is better than complex.

...'''


def test_trim_html_comment():
    assert trim_html_comment(SAMPLE_HTML) ==  EXPECTED_HTML
