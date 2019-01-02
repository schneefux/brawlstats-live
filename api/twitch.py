import logging
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

    def get_live_channel_names(self, game_id, limit=50):
        r = requests.get("https://api.twitch.tv/helix/streams",
                         params={
                             "first": limit,
                             "language": "en",
                             "game_id": game_id
                         }, headers=self._twitch_headers)
        return [data["user_name"] for data in r.json()["data"]]

    def get_stream(self, channel_name,
                   preferred_resolution=None):
        resolution_p = "{}p".format(preferred_resolution)
        try:
            streams = streamlink.streams(
                "https://www.twitch.tv/" + channel_name)
        except streamlink.exceptions.NoPluginError as err:
            logging.error(err)
            return None
        except streamlink.exceptions.PluginError as err:
            logging.error(err)
            return None
        if resolution_p in streams:
            return streams[resolution_p]
        else:
            logging.warning("configured resolution does not exist," +
                "scaling down best")
            if "best" in streams:
                return streams["best"]
            else:
                logging.error("'best' resolution does not exist")
                return None
