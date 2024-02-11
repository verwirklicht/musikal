# musikal
# by verwirklicht
# github.com/verwirklicht
# © 2024

print("[+] Loading...")

### CHANGE ME ###

pause_enabled = True # enable pause key
pause_key = "ALT" # key to pause music

clear_cmd = "cls" # command to clear terminal

## CHANGE ME ###

## banner

banner = """
                                     ███  █████                ████ 
                                           ███                  ███ 
 █████████████   █████ ████  █████  ████   ███ █████  ██████    ███ 
  ███  ███  ███   ███  ███  ███      ███   ███  ███       ███   ███ 
  ███  ███  ███   ███  ███   █████   ███   ██████     ███████   ███ 
  ███  ███  ███   ███  ███      ███  ███   ███  ███  ███  ███   ███ 
 █████ ███ █████   ████████ ██████  █████ ████ █████  ████████ █████
 by verwirklicht                             github.com/verwirklicht
 © 2024
"""


## imports

import asyncio
import os
import time
import pyautogui
import keyboard

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

## get current song info
async def get_info_async():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict["artist"] + " - " + info_dict["title"]
    return "No Song playing"

## async to non blocking
def get_info():
    try:
        return asyncio.run(get_info_async())
    except:
        return "No Song playing"

os.system("title musikal")

## main loop
current_song = ""
song_history = []
while True:
    old_song = current_song

    current_song = get_info()

    if not current_song == old_song: 
        os.system("cls")
        print(banner)
        if current_song == "No Song playing":
            print("[►] "+current_song)
        else:
            print("[►] Playing: "+current_song)
        print("[·] Pause Key: "+str(pause_key).upper())
        if not song_history == []:
            print()
            print("[+] History:")
            for song in song_history[::-1]:
                print(" - "+song)
        if not "Advertisement" in current_song and not len(current_song) <=5 and not current_song == "No Song playing":
            song_history.append(current_song)

    if pause_enabled and keyboard.is_pressed(pause_key):
        pyautogui.press("playpause")