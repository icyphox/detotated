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
            sendmsg(f"{user} is currently playing: {color(track, 'green')} by {color(artist, 'teal')}")
    except KeyError:
        sendmsg(color("smh there's nothing playing", "red"))

