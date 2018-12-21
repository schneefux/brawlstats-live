import requests
import streamlink

class TwitchAPIClient(object):
    def __init__(self, twitch_client_id):
        self._twitch_headers = { "Client-ID": twitch_client_id }

    def get_game_id(self, name):
        if name == "Brawl Stars":
            return "497497"
        r = requests.get(
            "https://api.twitch.tv/helix/games?name=" + name,
             headers=self._twitch_headers)
        return r.json()["data"][0]["id"]

    def get_live_channel_names(self, game_id):
        r = requests.get("https://api.twitch.tv/helix/streams" +
                         "?first=10&language=en&game_id=" + game_id,
                         headers=self._twitch_headers)
        return [data["user_name"] for data in r.json()["data"]]

    def get_stream(self, channel_name, resolution=None):
        resolution_p = "{}p".format(resolution)
        try:
            streams = streamlink.streams(
                "https://www.twitch.tv/" + channel_name)
        except streamlink.exceptions.NoPluginError as err:
            return None
        if resolution_p in streams:
            return streams[resolution_p]
        else:
            return None
