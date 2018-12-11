# coding=utf8

import os
import uuid
import requests
from jinja2 import Environment, FileSystemLoader

import re
templates_env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))


def _render_file(template_name, context, output_name, output_dir):
    template = templates_env.get_template(template_name)
    with open(os.path.join(output_dir, output_name), "w") as f:
        f.write(template.render(**context))


def _render_toc_md(title, headers,  output_dir):
    with open(os.path.join(output_dir, 'toc.md'), "w") as f:
        f.writelines([title] + headers)


def _render_article_html(title, content, output_dir):
    _render_file('article.html', {'title': title, 'content': content}, '{}.html'.format(title), output_dir)


def _format_file_name(name):
    return name.replace('/', '').replace(' ', '').replace('+', 'more').replace('"', '_')


def _generate_cover_img(url, output_dir):
    try:
        r = requests.get(url)
        with open(os.path.join(output_dir, 'cover.jpg'), 'wb') as f:
            f.write(r.content)
    except:
        # todo logging
        pass


def _parse_image(content, output_dir):

    p = r'img src="(.*?)"'
    img_url_list = re.findall(p, content, re.S)
    for url in img_url_list:
        try:
            url_local = str(uuid.uuid4()) + '.jpg'
            r = requests.get(url)
            with open(os.path.join(output_dir, url_local), 'wb') as f:
                f.write(r.content)
            content = content.replace(url, url_local)
        except:
            # todo logging
            pass
    return content






