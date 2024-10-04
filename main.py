from modules.tray import Tray
from modules.arduino import Arduino
from modules.color import SpotifyColorExtractor, Playback
from modules.utils import getNearestColorCode, isColorGrayscale

import os
import time
from colorist import rgb
import yaml


def RUN():
    arduino = Arduino("COM3")

    sp = SpotifyColorExtractor(
        clientID=os.getenv("CLIENT_ID"),
        clientSecret=os.getenv("CLIENT_SECRET"),
        redirectURI="http://localhost:50000/",
    )

    tray = Tray()

    lastAlbumID = None
    while tray.fRunning:
        playback = sp.getCurrentPlayback()

        if playback:
            currentAlbumID = playback.albumID

            if currentAlbumID != lastAlbumID:
                print(yaml.dump(playback.__dict__))

                mainColor = sp.extractMainColor(playback=playback, _logging=True)
                rgb(
                    f"\nBest color match: {mainColor}",
                    mainColor[0],
                    mainColor[1],
                    mainColor[2],
                )

                lastAlbumID = currentAlbumID

                if mainColor == (255, 255, 255):
                    print("COMMAND = 12.")

                    ardColor = mainColor
                    arduino.send("12.")
                else:
                    command, ardColor = getNearestColorCode(mainColor, _logging=True)

                    rgb(
                        f"MAIN COLOR: {ardColor}", ardColor[0], ardColor[1], ardColor[2]
                    )
                    print(f"COMMAND = {command}.")

                    arduino.send(f"{command}.")

                tray.spotify(playback=playback, color=ardColor)
        else:
            lastAlbumID = None
            print("No playback detected")

        time.sleep(2)


if __name__ == "__main__":
    RUN()
