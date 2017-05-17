import datetime
import tinyblobs
import json
from gmusicapi import Mobileclient

import argparse
parser = argparse.ArgumentParser(description='Backup your google play music playlists.')
parser.add_argument("username", help="google username")
parser.add_argument("password", help="google password")
parser.add_argument("archive", help="the backup archive")

args = parser.parse_args()

api = Mobileclient()
api.login(args.username, args.password, Mobileclient.FROM_MAC_ADDRESS)

with tinyblobs.open_stream(args.archive, "rb") as file:
    for playlist in file.iterJSON():
        tracks = playlist["tracks"]
        destPlaylistId = apiDest.create_playlist(playlist["name"], description=(playlist["description"] if "description" in playlist else None))
        print(apiDest.add_songs_to_playlist(destPlaylistId, [track["trackId"] for track in tracks]))
