# github_endpoints.py

import json
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

url = "https://docs.github.com/en/rest/overview/endpoints-available-for-github-app-installation-access-tokens?apiVersion=2022-11-28"

page = requests.get(url)
page.raise_for_status()

soup = BeautifulSoup(page.content, "html.parser")
links = soup.select("div.MarkdownContent_markdownBody__gRgTE li a")

endpoints: dict[str, list[str]] = defaultdict(list)
for link in links:
    method, url = link.text.split(" ")
    endpoints[method].append(url)

with open("endpoints.json", "w") as fp:
    json.dump(endpoints, fp)
