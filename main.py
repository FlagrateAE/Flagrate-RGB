from libs.tray import Tray
from libs.arduino import Arduino
from libs.color import SpotifyColorExtractor

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
import time

def RUN():
    arduino = Arduino("COM3")
    
    SpotifyColorExtractor()
    
    tray = Tray()
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                                client_secret=os.getenv("CLIENT_SECRET"),
                                                redirect_uri="http://localhost:50000/",
                                                scope="user-read-currently-playing user-read-playback-state"))

    print("Spotify connected")
    
    lastAlbumID = None
    while tray.fRunning:
        
        print(arduino.read())


if __name__ == "__main__":
    RUN()