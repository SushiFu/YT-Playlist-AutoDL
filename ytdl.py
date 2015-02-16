#!/usr/bin/env python

import pafy
import os
import time
import json

# Config
def createConfigFile():
    print("creating config")
    config_file = open("config", "w")
    youtube_playlist_url = input("Enter youtube playlist url : ")
    json_data = json.dumps({"urls": [youtube_playlist_url]})
    config_file.write(json_data)
    config_file.close()
    print("Config file created")
    return json_data

def getConfigData():
    if (fileCheck("config")):
        config_file = open("config", "r")
        json_data = json.loads(config_file.read())
        return json_data
    else:
        print("Error: no config")

# File function

def fileCheck(filename):
    try:
        open(filename, "r")
        return True
    except IOError:
        return False

# Playlist handle

def downloadPl(tracks):
    for t in tracks:
        print(t['pafy'].title)

        fout = playlist['title'].replace('/', '-') + '/' + t['pafy'].title.replace('/', '-') + ".mp3"
        if not os.path.isfile(fout):
            fout = "'" + fout + "'"
            s = t['pafy'].getbestaudio()
            f = s.download()
            fin = "'" + f + "'"
            conv = "ffmpeg -i "
            conv_args = " -threads 0 -codec:a libmp3lame -q:a 0 "
            print("Conversion en mp3")
            os.system(conv + fin + conv_args + fout + "> /dev/null 2>&1")
            print("\n")
            print("Suppression du fichier temporaire")
            os.remove(f)
        else:
            print("Deja Present")

def getComparePl(oldPlaylist, playlist):
    result = []

    for nt in playlist:
        isAlready = False
        for ot in oldPlaylist:
            if ot['pafy'].videoid == nt['pafy'].videoid:
                isAlready = True
                break
        if not isAlready:
            result.append(nt)

    return result

# Main

if __name__ == '__main__':

    # Check if config file exist, if not, create it
    fileExist = fileCheck("config")
    if (fileExist):
        print("Config file exist")
        json_data = getConfigData()
    else:
        print("Config file doesn't exist")
        json_data = createConfigFile()

    urls = json_data["urls"]
    firstURL = urls[0]

    playlist = pafy.get_playlist(firstURL)
    if not os.path.isdir(playlist['title'].replace('/', '-')):
        os.mkdir(playlist['title'].replace('/', '-'))

    print(playlist['title'] + "\n")
    print(playlist['author'] + "\n")
    downloadPl(playlist['items'])
    while True:
        oldPlaylist = list(playlist['items'])
        playlist = pafy.get_playlist(firstURL)
        newTracks = getComparePl(oldPlaylist, playlist['items'])
        print("New Tracks: " + str(len(newTracks)))
        downloadPl(newTracks)
        time.sleep(60 * 10)
