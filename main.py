from modules.tray import Tray
from modules.arduino import Arduino, get_nearest_color_code
from modules.spotify import SpotifyRequestHandler
from modules.color import Color, extract_main_color

import sys
import os
import time
from colorist import rgb
import yaml

def run(local_only = False, _logging = False):
    """Main function

    Parameters
    ----------
    local_only : bool
        Whether to only Python script Arduino (default: False)
        
    _logging : bool
        Whether to print advanced debug messages (default: False)
    """
    
    SPOTIFY_REQUEST_DELAY = 3
    
    
    if local_only:
        print("Starting in local-only mode")
    else:
        arduino = Arduino("COM3")
    if _logging:
        print("Advanced logging enabled")
        
    # initialize everything
    sp = SpotifyRequestHandler(
        os.environ["SPOTIFY_CLIENT_ID"],
        os.environ["SPOTIFY_CLIENT_SECRET"],
        os.environ["SPOTIFY_REDIRECT_URI"]
    )
    tray = Tray()

    last_album_id = True
    while tray.f_running:
        # get current playing track from Spotify
        playback: dict = sp.get_current_playback()

        if playback:
            # check if album has changed
            current_album_id = playback["album_id"]
            if current_album_id != last_album_id:

                if _logging:
                    print(yaml.dump(playback, allow_unicode=True))
                else:
                    print(
                        f'Now playing "{playback["artist"]} - {playback["track"]}" from album "{playback["album_name"]}"'
                    )

                # get main color
                main_color = extract_main_color(playback["image_url"], _logging)
                last_album_id = current_album_id

                if _logging:
                    rgb(
                        f"\nBest color from image: {main_color}",
                        main_color[0],
                        main_color[1],
                        main_color[2],
                    )

                if main_color is Color.WHITE:
                    color_led = main_color
                    command = 12
                else:
                    # get my color code for RGB LED
                    command, color_led = get_nearest_color_code(main_color, _logging)

                # display color in console and tray
                rgb(f"MAIN COLOR: {color_led}\n", color_led[0], color_led[1], color_led[2])
                tray.spotify(playback, color_led)
                
                if not local_only:
                    # execute color command transmittion
                    print(f"SENT COMMAND: {command}.\n")
                    arduino.send(f"{command}.")
        else:
            if last_album_id:
                print("No playback detected")
                last_album_id = None

        time.sleep(SPOTIFY_REQUEST_DELAY)


if __name__ == "__main__":
    # parse arguments
    local_only = True if "--local-only" in sys.argv else False
    _logging = True if "--log" in sys.argv else False
    
    run(local_only, _logging)
