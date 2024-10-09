from modules.tray import Tray
from modules.arduino import Arduino
from modules.color import SpotifyColorExtractor, Playback
from modules.utils import getNearestColorCode

import sys
import os
import time
from colorist import rgb
import yaml


def RUN(localOnly = False, _logging = False):
    """Main function

    Parameters
    ----------
    localOnly : bool
        Whether to only Python script Arduino (default: False)
    
    _logging : bool
        Whether to print advanced debug messages (default: False)
    """
    
    if localOnly:
        print("Starting in local-only mode")
    else:
        arduino = Arduino("COM3")
    if _logging:
        print("Advanced logging enabled")
        
    # initialize everything
    sp = SpotifyColorExtractor(
        clientID=os.getenv("SPOTIFY_CLIENT_ID"),
        clientSecret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirectURI=os.getenv("SPOTIFY_REDIRECT_URI"),
    )
    tray = Tray()

    lastAlbumID = True
    while tray.fRunning:
        # get current playing track from Spotify
        playback: Playback = sp.getCurrentPlayback()

        if playback:
            # check if album has changed
            currentAlbumID = playback.albumID
            if currentAlbumID != lastAlbumID:

                if _logging:
                    print(yaml.dump(playback.__dict__))
                else:
                    print(
                        f'Now playing "{playback.artist} - {playback.track}" from album "{playback.albumName}"'
                    )

                # get main color
                mainColor = sp.extractMainColor(playback=playback, _logging=_logging)
                lastAlbumID = currentAlbumID

                if _logging:
                    rgb(
                        f"\nBest color from image: {mainColor}",
                        mainColor[0],
                        mainColor[1],
                        mainColor[2],
                    )

                if mainColor == (255, 255, 255):
                    LEDColor = (255, 255, 255)
                    command = 12
                else:
                    # get my color code for RGB LED
                    command, LEDColor = getNearestColorCode(mainColor, _logging)

                # display color in console and tray
                rgb(f"MAIN COLOR: {LEDColor}\n", LEDColor[0], LEDColor[1], LEDColor[2])
                tray.spotify(playback=playback, color=LEDColor)
                
                if not localOnly:
                    # execute color command transmittion
                    print(f"SENT COMMAND: {command}.\n")
                    arduino.send(f"{command}.")
        else:
            if lastAlbumID:
                print("No playback detected")
                lastAlbumID = None

        time.sleep(2)


if __name__ == "__main__":
    # parse arguments
    localOnly = True if "--local-only" in sys.argv else False
    _logging = True if "--log" in sys.argv else False
    
    RUN(localOnly, _logging)
