#!/usr/bin/env python3
# "how much detotated wam do you need for a server?"
# detotated - irc bot for #crimson; you are not welcome
# Anirudh <x@icyphox.sh>

import socket
import os
import requests
import re
import metadata_parser

SERVER = "irc.rizon.net"
CHANNELS = ["#crimbot", "#crimson"]
NICK = "detotated"
PASSWORD = os.environ.get("DETOTATED_PW")
SENT_NICK = False
SENT_USER = False


def b(s):
    print(f"log: {s}")
    return s.encode("UTF-8")


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((SERVER, 6667))


def send_nick():
    irc.send(b(f"NICK {NICK}\n"))


def send_user():
    irc.send(b(f"USER {NICK} {NICK} {NICK} :{NICK}\n"))


def joinchan():
    for c in CHANNELS:
        irc.send(b(f"JOIN {c}\n"))
    sendmsg("how much detotated wam do you need for a server?")


def sendmsg(msg, target="#crimson"):
    irc.send(b(f"PRIVMSG {target} :{msg}\n"))


def lastfm(user):
    API_KEY = "767dc7e260f5facfe2a6f39496983d5b"
    USER = user
    URL = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={USER}&api_key={API_KEY}&format=json&limit=1&nowplaying=true"
    r = requests.get(URL)
    data = r.json()
    print(data)
    try:
        if data["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
            track = data["recenttracks"]["track"][0]["name"]
            artist = data["recenttracks"]["track"][0]["artist"]["#text"]
            sendmsg(f"{user} is currently playing: {track} by {artist}")
    except KeyError:
        sendmsg(f"you are not playing anything")


def findurls(message):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    for u in urls:
        page = metadata_parser.MetadataParser(url=u, search_head_only=False)
        title = page.get_metadatas('title', strategy=['og'])
        if title:
            sendmsg(f"{u}: {title}")


if __name__ == "__main__":
    try:
        while True:
            ircmsg = ""
            ircmsg = irc.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip("\n\r")

            if len(ircmsg) > 0:
                print(ircmsg)
                findurls(ircmsg)
            else:
                continue

            if ircmsg.find("PING :") != -1:
                irc.send(b(f"PONG {ircmsg.split()[1]}\n"))

            if SENT_USER == False:
                send_user()
                SENT_USER = True
                continue

            if SENT_NICK == False:
                send_nick()
                SENT_NICK = True
                continue

            if ircmsg.find(f"255 {NICK}") != -1:
                irc.send(b(f"NickServ identify {PASSWORD}\r\n"))
                joinchan()

            if ircmsg.find("PRIVMSG") != -1:
                username = ircmsg.split("!", 1)[0][1:]
                message = ircmsg.split("PRIVMSG", 1)[1].split(":", 1)[1]
                if message.find(f"{NICK}") != -1:
                    sendmsg(f"sup mah nigatoni {username}!")
                if message[:3].find(".np") != -1:
                    lastfm(username)
    except KeyboardInterrupt:
        sendmsg("kthx bye")
