from modules.tray import Tray
from modules.arduino import Arduino
from modules.color import SpotifyColorExtractor, Playback
from modules.utils import getNearestColorCode, isColorGrayscale

import os
import time
from colorist import rgb
import yaml


def RUN(_logging=False):
    """Main function

    Parameters
    ----------
    _logging : bool
        Whether to print advanced debug messages (default: False)
    """

    # initialize everything
    arduino = Arduino("COM3")
    sp = SpotifyColorExtractor(
        clientID=os.getenv("CLIENT_ID"),
        clientSecret=os.getenv("CLIENT_SECRET"),
        redirectURI="http://localhost:50000/",
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
                        f'Now playing: {playback.artist} - {playback.track} from "{playback.albumName}"'
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
                    command, LEDColor = getNearestColorCode(mainColor, _logging=True)

                # execute color transmission and display in console and tray
                print(f"COMMAND = {command}.\n")
                arduino.send(f"{command}.")
                rgb(f"COLOR SENT: {LEDColor}", LEDColor[0], LEDColor[1], LEDColor[2])
                tray.spotify(playback=playback, color=LEDColor)
        else:
            if lastAlbumID:
                print("No playback detected")
                lastAlbumID = None

        time.sleep(2)


if __name__ == "__main__":
    RUN(_logging=True)
