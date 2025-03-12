# coding=utf8
import requests


# 推送消息(Markdown)
def send_markdown_msg(webhook, content):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content,
        }
    }
    requests.post(url=webhook, json=data)
