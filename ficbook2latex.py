#!/usr/bin/env python3
import re

import requests
from bs4 import BeautifulSoup


def main(url):
    r = requests.get(url)
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
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')

        text = ''.join(map(str, soup.select('div#content')[0].contents))

        text = text.replace('<br/>', '').replace('\r', '')
        text = text.replace('<p align="center" style="margin: 0px;">***</p>', r'\begin{center}* * *\end{center}')
        text = re.sub(r'<i>(.+?)</i>', r'\\textit{\1}', text)
        text = text.replace('а́', r'\textit{а}')
        text = text.replace('á', r'\textit{а}')
        text = text.replace('о́', r'\textit{о}')
        text = text.replace('я́', r'\textit{я}')
        text = text.replace('е́', r'\textit{е}')
        text = text.replace('у́́', r'\textit{у}')

        context['chapters'].append(r'''
\chapter{%s}
\thispagestyle{empty}
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
    main(url='https://ficbook.net/readfic/8251369')
