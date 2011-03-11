import cgi
from pytm import webpreview


def escape_for_html(txt):
    return cgi.escape(txt or '').encode('ascii', 'xmlcharrefreplace')


def header(title, subtitle=''):
    return webpreview.html_header(title, subtitle)


def footer():
    return webpreview.html_footer()
