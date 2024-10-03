from libs.tray import Tray
from libs.arduino import Arduino, _getNearestColorCode
from libs.color import SpotifyColorExtractor

import os
import time
from colorist import rgb

def RUN():
    arduino = Arduino("COM3")
    
    sp = SpotifyColorExtractor(clientID=os.getenv("CLIENT_ID"),
                                clientSecret=os.getenv("CLIENT_SECRET"),
                                redirectURI="http://localhost:50000/")
    
    tray = Tray()
    
    lastAlbumID = None
    while tray.fRunning:
        
        currentlyPlaying = sp.getCurrentPlayback()
        
        if currentlyPlaying:
            currentAlbumID = currentlyPlaying[1]
            
            if currentAlbumID != lastAlbumID:
                print(currentlyPlaying)
                
                mainColor = sp.extractMainColor(currentlyPlaying[2], True)
                rgb(f"Main color exctracted: {mainColor}", mainColor[0], mainColor[1], mainColor[2])
                
                lastAlbumID = currentAlbumID
                
                if mainColor == (255, 255, 255):
                    print("COMMAND = 12.")
                    
                    arduino.send("12.")
                else:
                    command, ardColor = _getNearestColorCode(mainColor)
                    
                    rgb(f"MAIN COLOR: {ardColor}", ardColor[0], ardColor[1], ardColor[2])
                    print(f"COMMAND = {command}.")
                    
                    arduino.send(f"{command}.")

            else:
                time.sleep(2)
                continue
        else:
            lastAlbumID = None
            print("No playback detected")
            
        time.sleep(2)


if __name__ == "__main__":
    RUN()