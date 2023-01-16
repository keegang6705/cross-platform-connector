linetoken=""
linesecret=""
discordwebhook=""


import discord
import os
import json
import pytz
from datetime import datetime
from flask import Flask, request, abort
from discord import SyncWebhook, Embed
from threading import Thread
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
webhook = SyncWebhook.from_url(url=discordwebhook)
app = Flask(__name__)
def date():
    tz = pytz.timezone('Asia/Bangkok')
    tm = datetime.now(tz)
    sak = int(tm.strftime("%G"))+543
    tmfs = tm.strftime(f"%A %d %B(%m) {sak}(%G) | %H:%M:%S.%f")[:-4]
    return tmfs
@app.route('/')
def main():
    return "a bot is running"
def run():
    app.run(host="0.0.0.0", port=8000)
def keep_alive():
    server = Thread(target=run)
    server.start()
keep_alive()

line_bot_api = LineBotApi(linetoken)
handler = WebhookHandler(linesecret)


@app.route("/webhook", methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    print(decoded)
    profile = line_bot_api.get_profile(decoded["events"][0]["source"]["userId"])
    if decoded["events"][0]["source"]["type"] == "group":
        summary = line_bot_api.get_group_summary(decoded["events"][0]["source"]["groupId"])
        if decoded["events"][0]["message"]["type"] == "text":
            try:
                if len(decoded["events"][0]["message"]["text"]) <= 256:
                    embed = discord.Embed(title=decoded["events"][0]["message"]["text"],
                                        description=f"message from `{summary.group_name}`", color=0x00ff00)
                    embed.set_author(name=profile.display_name,
                                    icon_url=profile.picture_url)
                    embed.set_footer(text=date())
                    webhook.send(embed=embed)
                else:
                    embed = discord.Embed(title="too long(>256) cut to new message",
                                        description=f"message from `{summary.group_name}`", color=0x00ff00)
                    embed.set_author(name=profile.display_name,
                                    icon_url=profile.picture_url)
                    embed.set_footer(text=date())
                    webhook.send(embed=embed)
                    if len(decoded["events"][0]["message"]["text"]) <= 2000:
                        webhook.send(content=decoded["events"][0]["message"]["text"])
                    else:
                        chunks, chunk_size = len(decoded["events"][0]["message"]["text"]), 2000
                        for x in [ (decoded["events"][0]["message"]["text"])[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]:
                            webhook.send(x)
            except Exception as e:
                print(e)
                print("error but don't worry i response as 200")
        elif decoded["events"][0]["message"]["type"] == "image":
            try:
                message_content = line_bot_api.get_message_content(
                    decoded["events"][0]["message"]["id"])
                with open('file.jpg', 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)
                    fd.close
                embed = discord.Embed(title=f"user `{profile.display_name}` send image",
                                      description=f"message from `{summary.group_name}`", color=0x00ff00)
                embed.set_author(name=profile.display_name,
                                 icon_url=profile.picture_url)
                embed.set_footer(text=date())
                webhook.send(embed=embed)
                with open('file.jpg', 'rb') as f:
                    picture = discord.File(f)
                    webhook.send(file=picture)
            except Exception as e:
                print(e)
                print("error but don't worry i response as 200")
    elif decoded["events"][0]["source"]["type"] == "user":
        if decoded["events"][0]["message"]["type"] == "text":
            try:
                if len(decoded["events"][0]["message"]["text"]) <= 256:
                    embed = discord.Embed(title=decoded["events"][0]["message"]["text"],
                                        description="", color=0x00ff00)
                    embed.set_author(name=profile.display_name,
                                    icon_url=profile.picture_url)
                    embed.set_footer(text=date())
                    webhook.send(embed=embed)
                else:
                    embed = discord.Embed(title="too long(>256) cut to new message",
                                        description="", color=0x00ff00)
                    embed.set_author(name=profile.display_name,
                                    icon_url=profile.picture_url)
                    embed.set_footer(text=date())
                    webhook.send(embed=embed)
                    if len(decoded["events"][0]["message"]["text"]) <= 2000:
                        webhook.send(content=decoded["events"][0]["message"]["text"])
                    else:
                        chunks, chunk_size = len(decoded["events"][0]["message"]["text"]), 2000
                        for x in [ (decoded["events"][0]["message"]["text"])[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]:
                            webhook.send(x)
            except Exception as e:
                print(e)
                print("error but don't worry i response as 200")
        elif decoded["events"][0]["message"]["type"] == "image":
            try:
                message_content = line_bot_api.get_message_content(
                    decoded["events"][0]["message"]["id"])
                with open('file.jpg', 'wb') as fd:
                    for chunk in message_content.iter_content():
                        fd.write(chunk)
                    fd.close
                embed = discord.Embed(title=f"user `{profile.display_name}` send image",
                                      description="", color=0x00ff00)
                embed.set_author(name=profile.display_name,
                                 icon_url=profile.picture_url)
                embed.set_footer(text=date())
                webhook.send(embed=embed)
                with open('file.jpg', 'rb') as f:
                    picture = discord.File(f)
                    webhook.send(file=picture)
            except Exception as e:
                print(e)
                print("error but don't worry i response as 200")
    print("from callback")
    return "", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    print("from handle")


if __name__ == "__main__":
    app.run()
