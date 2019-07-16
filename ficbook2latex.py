#!/usr/bin/env python3
import re
import logging
# noinspection PyUnresolvedReferences
import setuplogging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


def main(url):
    s = requests.Session()
    r = s.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')

    context = {
        'title': soup.select('title')[0].text.split('\n')[0].strip(),
        'author': soup.select('a.avatar-nickname')[0].text,
        'description': soup.select('div.description')[0].text.replace('<br/><br/>', '\n\n'),
        'url': url,
        'chapters': [],
    }

    for i in soup.select('a.visit-link'):
        url = 'https://ficbook.net' + i['href']
        r = s.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')
        tag = soup.select('div#content')[0]
        for j in tag.find_all('i'):
            j.string = '\\textit{%s}' % j.string.replace('\r\n\r\n', '}\n\n\\textit{')

        text = str(tag)

        # text = ''.join(map(str, .contents))

        # text = text.replace('<br/>', '').replace('\r', '')
        text = text.replace('<p align="center" style="margin: 0px;">***</p>', r'''
\vspace{12pt}
\centerline{* * *}''')
        # <p align="center" style="margin: 0;">* * *</p>
        text = text.replace('_', r'\\_')
        text = text.replace('&', r'\\&')

        # def f(m):
        #     t = m.group(1)
        #     print(t)
        #     return '\\textit{%s}' % t.replace('\n', '}\n\\textit{')
        #
        # text = re.sub(r'<i>(.+?)</i>', f, text)
        # text = re.sub(r'<b>(.+?)</b>', r'\\textibf\1}', text)

        # text = text.replace('а́', r'\textit{а}')
        # text = text.replace('á', r'\textit{а}')
        # text = text.replace('о́', r'\textit{о}')
        # text = text.replace('я́', r'\textit{я}')
        # text = text.replace('е́', r'\textit{е}')
        # text = text.replace('у́́', r'\textit{у}')

        context['chapters'].append(r'''
\newpage
\section{%s}
%s''' % (soup.select('h2')[0].text, text))

    context['chapters'] = '\n\n\n\n'.join(context['chapters'])
    save(context)


def save(context):
    with open('template.tex') as f:
        t = f.read()

    for k, v in context.items():
        t = t.replace('##%s##' % k, v)

    with open('out.tex', 'w') as f:
        f.write(t)


if __name__ == '__main__':
    main(url='https://ficbook.net/readfic/8016580')
