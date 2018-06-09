#!/usr/bin/env python3
import re
import argparse


def main(text):
    with open('template.tex') as f:
        out = f.read()

    for k, v in get_context(text).items():
        out = out.replace('##%s##' % k, v)

    with open('out.tex', 'w') as f:
        f.write(out)


def get_context(text):
    header, body = re.split(r'={10}', text, 1)
    body = '='*10 + body
    body = re.sub(r'={10}\s(.*?)\s={10}', r'\section{\1}', body)
    # \begin{center}* * *\end{center}\vspace{-1em}
    body = body.replace('_', '\_')

    ls = header.split('\n', 25)
    return {
        'author': re.findall(r'Автор:\s(.*?)\s\(', header, re.UNICODE)[0],
        'title': ls[1],
        'description': ls[19],
        'body': body,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename) as f:
        main(f.read())
