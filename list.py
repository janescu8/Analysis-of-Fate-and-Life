#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 16:03:51 2025

@author: luoshanni
"""

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Time_100"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 找出所有 .gallerybox 區塊
gallery_boxes = soup.find_all("div", class_="gallerytext")

names = []

for box in gallery_boxes:
    a_tag = box.find("a")  # 抓第一個 a 標籤
    if a_tag and a_tag.text.strip():
        names.append(a_tag.text.strip())

# 印出結果
for name in names:
    print(name)


