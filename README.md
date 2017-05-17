# Google Music Playlist Backup
A tool for backing up your playlists with google music!

Two scripts are included:
```
python google-backup-playlists.py
python google-restore-playlists.py
```
the backug script produces a json.gz (gzip'd) file in the directory it is run from containing your playlists in its compressed archive format. 

the restore script will, given your credentials and the path to a backup archive, restore the playlists in the archive to the currently logged in account.

Pardon the brief explanation. Create an issue if you'd like more details. Until I see this getting used its primarily for personal use :)
