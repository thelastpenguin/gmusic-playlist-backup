import datetime
import tinyblobs
import json
from gmusicapi import Mobileclient

import argparse
parser = argparse.ArgumentParser(description='Backup your google play music playlists.')
parser.add_argument("username", help="google username")
parser.add_argument("password", help="google password")

args = parser.parse_args()

api = Mobileclient()
api.login(args.username, args.password, Mobileclient.FROM_MAC_ADDRESS)

with tinyblobs.open_stream("playlists-backup-%s.json.gz" % (datetime.datetime.now().strftime("%Y-%m-%d %H-%M")), "wb", compresslevel=9) as backup:
    for playlist in api.get_all_user_playlist_contents():
        playlist["tracks"] = [track for track in playlist["tracks"]]
        backup.writeString(json.dumps(playlist, indent=4))
