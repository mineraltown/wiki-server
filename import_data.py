import os
import re
import requests
import django
from pathlib import Path


def remove_newline_and_whitespace(text):
    """
    去除换行符后的空白及换行符本身
    """
    return re.sub(r"\n\s*", "", text)


def read_file(r):
    """
    读取文件
    read_file("test.txt")
    """
    with open(r, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def get_json(url):
    """
    读取 .json 文件
    get_json("https://wiki.mineraltown.net/saikai/Tools/Fish.json")
    """
    r = requests.get(url).json()
    return r


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki.settings")  # wsgi.py
django.setup()

from index.models import *
from saikai.models import *

print("=" * 20)
v = version.objects.get(id=34)  # 版本《重聚矿石镇》
print(v)
print("-" * 20)

"""
n = 100
dir = Path.cwd() / "Library"
for html in dir.glob("*.html"):
    n-=1
    f = html.read_text(encoding="utf-8")
    a = f.split("<body>")[-1].split("</h1>")
    title = a[0].split("<h1>")[-1]
    text = (
        remove_newline_and_whitespace(a[-1].split("</body>")[0])
        .replace("<h2>", '<h2 class="h2">')
        .replace("<p>", '<p class="p">')
        .replace("<ul>", '<ul class="ul">')
        .replace("<li>", '<li class="li">')
        .replace("<h3>", '<h3 class="h3">')
        .replace("<ol>", '<ol class="ol">')
    )
    print(title)
    c = content.objects.create(
        title=title,
        text=text,
    )
    to.objects.create(
        title=title,
        version=v,
        parent=p,
        link=c,
        sort=n,
    )
"""

"""
l = read_file("test.html")
n = 100
for i in l:
    n-=1
    x = i.split("</h3>")
    y = x[0].split(">")[-1]
    z = remove_newline_and_whitespace(x[1].strip("\n"))
        .replace("<b>","<strong>")
        .replace("</b>","</strong>")
    c = content.objects.create(
        title=y,
        text=z,
    )
    to.objects.create(
        title=y,
        version=v,
        parent=p,
        link=c,
        sort=n,
    )
"""

"""
for i in resident.objects.filter(form="O"):
    print(i.name)
"""
