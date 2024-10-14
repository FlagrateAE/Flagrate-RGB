from modules.tray import Tray
from modules.arduino import Arduino
from modules.color import SpotifyColorExtractor, Playback
from modules.utils import get_nearest_color_code

import sys
import os
import time
from colorist import rgb
import yaml

def RUN(local_only = False, _logging = False):
    """Main function

    Parameters
    ----------
    local_only : bool
        Whether to only Python script Arduino (default: False)
        
    _logging : bool
        Whether to print advanced debug messages (default: False)
    """
    
    if local_only:
        print("Starting in local-only mode")
    else:
        arduino = Arduino("COM3")
    if _logging:
        print("Advanced logging enabled")
        
    # initialize everything
    sp = SpotifyColorExtractor(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    )
    tray = Tray()

    last_album_id = True
    while tray.f_running:
        # get current playing track from Spotify
        playback: Playback = sp.getCurrentPlayback()

        if playback:
            # check if album has changed
            current_album_id = playback.album_id
            if current_album_id != last_album_id:

                if _logging:
                    print(yaml.dump(playback.__dict__))
                else:
                    print(
                        f'Now playing "{playback.artist} - {playback.track}" from album "{playback.album_name}"'
                    )

                # get main color
                mainColor = sp.extractMainColor(playback=playback, _logging=_logging)
                last_album_id = current_album_id

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
                    command, LEDColor = get_nearest_color_code(mainColor, _logging)

                # display color in console and tray
                rgb(f"MAIN COLOR: {LEDColor}\n", LEDColor[0], LEDColor[1], LEDColor[2])
                tray.spotify(playback=playback, color=LEDColor)
                
                if not local_only:
                    # execute color command transmittion
                    print(f"SENT COMMAND: {command}.\n")
                    arduino.send(f"{command}.")
        else:
            if last_album_id:
                print("No playback detected")
                last_album_id = None

        time.sleep(2)


if __name__ == "__main__":
    # parse arguments
    localOnly = True if "--local-only" in sys.argv else False
    _logging = True if "--log" in sys.argv else False
    
    RUN(localOnly, _logging)
