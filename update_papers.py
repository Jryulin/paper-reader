#!/usr/bin/env python3
"""
將 papers.json 注入 index.html，並自動 commit + push 到 GitHub。
每次新增/修改論文後執行此腳本即可同步網頁。
"""

import json, re, os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE, "papers.json")
HTML_PATH = os.path.join(BASE, "index.html")


def inject_html():
    with open(JSON_PATH) as f:
        papers = json.load(f)
    with open(HTML_PATH) as f:
        html = f.read()
    new_data = f"const PAPERS_DATA = {json.dumps(papers, ensure_ascii=False, indent=2)};"
    html = re.sub(r"const PAPERS_DATA = \[.*?\];", new_data, html, flags=re.DOTALL)
    with open(HTML_PATH, "w") as f:
        f.write(html)
    return len(papers)


def git(cmd, check=True):
    result = subprocess.run(
        ["git"] + cmd, cwd=BASE, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"git {' '.join(cmd)} 失敗：{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def deploy(message=None):
    count = inject_html()
    print(f"✅ index.html 已注入 {count} 篇論文")

    # 確認有變更
    status = git(["status", "--porcelain"])
    if not status:
        print("ℹ️  沒有變更，無需 commit")
        return

    # commit
    if not message:
        message = f"Auto-sync: {count} papers"
    git(["add", "papers.json", "index.html", "update_papers.py"])
    git(["commit", "-m", message])
    print(f"✅ 已 commit：{message}")

    # pull rebase + push
    git(["pull", "--rebase", "origin", "main"])
    git(["push", "origin", "main"])
    print("✅ 已 push 到 GitHub")


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or None
    deploy(msg)
