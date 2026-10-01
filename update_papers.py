#!/usr/bin/env python3
"""將 papers.json 注入 index.html，確保離線/file:// 也能正確顯示所有論文"""

import json, re, os

BASE = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE, "papers.json")
HTML_PATH = os.path.join(BASE, "index.html")

with open(JSON_PATH) as f:
    papers = json.load(f)

with open(HTML_PATH) as f:
    html = f.read()

new_data = f"const PAPERS_DATA = {json.dumps(papers, ensure_ascii=False, indent=2)};"
html = re.sub(r"const PAPERS_DATA = \[.*?\];", new_data, html, flags=re.DOTALL)

with open(HTML_PATH, "w") as f:
    f.write(html)

print(f"✅ index.html 已更新：{len(papers)} 篇論文")
