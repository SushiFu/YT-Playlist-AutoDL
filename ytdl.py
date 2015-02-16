#!/usr/bin/env python

import pafy
import os
import sys
import time

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
            conv_args = " -codec:a libmp3lame -q:a 0 "
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

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Enter a url playlist, Usage: " + sys.argv[0] + " url")
        exit(1)

    playlist = pafy.get_playlist(sys.argv[1])
    if not os.path.isdir(playlist['title'].replace('/', '-')):
        os.mkdir(playlist['title'].replace('/', '-'))

    print(playlist['title'] + "\n")
    print(playlist['author'] + "\n")
    downloadPl(playlist['items'])
    while True:
        oldPlaylist = list(playlist['items'])
        playlist = pafy.get_playlist(sys.argv[1])
        newTracks = getComparePl(oldPlaylist, playlist['items'])
        print("New Tracks: " + str(len(newTracks)))
        downloadPl(newTracks)
        time.sleep(10)


