# LAST.FM API script - https://www.last.fm/api
 
import requests
from pprint import pprint

apiData = {
    "artists": {
        "method": "user.getTopArtists",
        "root": "topartists",
        "table": "artist"
    },
    "albums": {
        "method": "user.getTopAlbums",
        "root": "topalbums",
        "table": "album"
    },
    "tracks": {
        "method": "user.getTopTracks",
        "root": "toptracks",
        "table": "track"
    },
    "lovedtracks": {
        "method": "user.getLovedTracks",
        "root": "lovedtracks",
        "table": "track"
    },
    "recenttracks": {
        "method": "user.getRecentTracks",
        "root": "recenttracks",
        "table": "track"
    },
}

class LastfmApi():

    def __init__(self, user, apiKey):
        self.user = user
        self.apiKey = apiKey

    def query(self, method, page = 1, pageSize = 100):
        return requests.request("GET", "https://ws.audioscrobbler.com/2.0/", params={
            "api_key": self.apiKey,
            "format": "json",
            "user": self.user,
            "method": method,
            "limit": str(pageSize),
            "page": str(page)
            })

    def generator(self, type, page = 1, limit = 10):
        count = 0

        method = apiData[type]["method"]
        rootKey = apiData[type]["root"]
        tableKey = apiData[type]["table"]

        while True:
            r = self.query(method, page)
            json_object = r.json()

            if page > int(json_object[rootKey]["@attr"]["totalPages"]):
                return

            for obj in json_object[rootKey][tableKey]:
                if count <= limit:
                    yield obj
                    count += 1
                else:
                    return
            page += 1


          

# SCRIPT

api = LastfmApi("YOUR_USERNAME", "YOUR_LASTFM_APIKEY")

userInfo = api.query("user.getInfo").json()
pprint(userInfo)


''' Examples

# Top artists
for obj in api.generator("artists"):
    print(obj["name"])

# Top albums
for obj in api.generator("albums"):
    print(obj["name"])

# Top tracks
for obj in api.generator("tracks"):
    print(obj["name"])

'''
