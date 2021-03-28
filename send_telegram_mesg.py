#!/usr/bin/env python3
"""
Wrapper for Telegram messages bot
Author: Jose Vicente Nunez
"""
import sys
import os
import requests
import pprint

BOT_CONFIG = {
    "chat_id": os.environ['TELEGRAM_CHAT_ID'],
    "name": os.environ['TELEGRAM_NAME'],
    "username": os.environ['TELEGRAM_USERNAME'],
    "api_key": os.environ['TELEGRAM_API_KEY'],
    "base_url": "https://api.telegram.org",
    "disable_web_page_preview": True,
    "parse_mode": "MarkdownV2",
    "disable_notification": True,
    "allow_sending_without_reply": True
}

def escape_chars(message):
    return message\
            .replace(".", "\\.")\
            .replace("*", "\\*")\
            .replace("[", "\\[")\
            .replace("]", "\\]")\
            .replace("(", "\\(")\
            .replace(")", "\\)")\
            .replace("-", "\\-")\
            .replace("`", "\\`")

def sendMessage(message:str):
    """
    :param str message
    """
    payload = {
                "chat_id": BOT_CONFIG["chat_id"],
                "parse_mode": BOT_CONFIG["parse_mode"],
                "disable_web_page_preview": BOT_CONFIG["disable_web_page_preview"],
                "parse_mode": BOT_CONFIG["parse_mode"],
                "disable_notification": BOT_CONFIG["disable_notification"],
                "allow_sending_without_reply": BOT_CONFIG["allow_sending_without_reply"],
                "text": escape_chars(message),
            }
    url = "{base_url}/bot{api_key}/sendMessage".format_map(BOT_CONFIG)
    response = requests.get(url, params=payload)
    return response.json()

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    result = sendMessage(" ".join(sys.argv[1:]))
    if not result['ok']:
        pp.pprint("ERROR: {}".format(BOT_CONFIG))
    pp.pprint("Response: {}".format(result))
