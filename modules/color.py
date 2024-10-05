import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

from colorist import rgb, hsl as hls
from Pylette import extract_colors

import modules.utils as utils
from modules.utils import Playback


class SpotifyColorExtractor:
    def __init__(self, clientID: str, clientSecret: str, redirectURI: str):
        """Connect to Spotify

        Parameters
        ----------
        clientID : str
            Spotify client ID
        clientSecret : str
            Spotify client secret
        redirectURI : str
            Spotify redirect URI

        Those should be acquired from https://developer.spotify.com/dashboard
        """
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=clientID,
                client_secret=clientSecret,
                redirect_uri=redirectURI,
                scope="user-read-currently-playing user-read-playback-state",
            )
        )

        print("Spotify connected")

    def getCurrentPlayback(self) -> Playback | None:
        """Get current playing track necessary information

        Parameters
        ----------
        _logging : bool
            Whether to print advanced debug messages (default: False)

        Returns
        -------
        Playback : if track is playing
        None : if no track is playing
        """

        result = self.client.current_playback()

        try:
            playback = Playback(result)
            return playback
        except:
            return None

    def extractMainColor(
        self, playback: Playback, imageURL: str = None, _logging: bool = False
    ) -> tuple[int, int, int]:
        """
        Extract most vibrant color from Spotify album cover image

        Parameters
        ----------
        playback : Playback
            Spotify current playback
        imageURL : str
            For cases if you want to extract the main color outside of Spotify (default: None)
        _logging : bool
            Whether to print advanced debug messages (default: False)

        Returns
        -------
        tuple : (R, G, B)

        Note
        ----
        This function is suited for displaying color on RGB LED. Thus, vibrant colors are meant to be further exagerrated because dark colors on RGB LED look poor (for example, to display brown, you have to dim the orange). For the same reason any grayscale colors are displayed as white.
        """

        if playback:
            imageURL = playback.imageURL
        elif not imageURL:
            raise ValueError("No image URL provided")
        
        
        # extract main 5 colors palette from smaller image
        palette = extract_colors(image=imageURL, palette_size=5).colors
        vibrantPalette = [] # here will be colors suitable for further processing
        
        if _logging: print("Colors extracted for grayscale check (RGB):")
        
        for paletteColor in palette:
            paletteRGB = tuple(paletteColor.rgb)
            if _logging: rgb(f"{paletteRGB}", paletteRGB[0], paletteRGB[1], paletteRGB[2])
            
            # check if each color is grayscale
            if utils.isColorGrayscale(paletteRGB):
                print("Grayscale")
            else:
                vibrantPalette.append(paletteRGB)
                print("Not grayscale")
        
        # proceed with HLS threshold analysis
        if not vibrantPalette:
            if _logging: print("The image is grayscale")
            return (255, 255, 255)
        else:
            if _logging: print("\nHLS threshold analysis:")
          
        for color in vibrantPalette.copy():
            paletteHLS = utils.RGB2HLS(color)
            
            if paletteHLS[1] < 15 or paletteHLS[1] > 85: # too dark ot too bright
                msg = "too dark or too bright"
                vibrantPalette.remove(color)
            elif paletteHLS[2] < 15: # too unvibrant
                msg = "too unvibrant"
                vibrantPalette.remove(color)
            else:
                msg = "appropriate"
                
            if _logging: hls(f"{paletteHLS} - {msg}", paletteHLS[0], paletteHLS[1], paletteHLS[2])
        
        if not vibrantPalette:
            return (255, 255, 255)
            
        if _logging:
            print("\nFinal vibrant palette in RGB:")
            for color in vibrantPalette:
                rgb(f"{color}", color[0], color[1], color[2])

        # if not grayscale, get vibrant and muted colors from flagrate vibrant api
        imageID = imageURL.split("/")[-1]
        apiColors: dict = requests.get(
            url="https://flagrate-vibrant-api.vercel.app?icon_id=" + imageID,
            headers={"Accept": "application/json"},
        ).json()
        
        if _logging:
            print("\nColors extracted by API:")
            for name, apiColor in apiColors.items():
                rgb(
                    f"{name}: {tuple(apiColor)}",
                    apiColor[0],
                    apiColor[1],
                    apiColor[2]
                )

        # searching for 
        for paletteColor in vibrantPalette:
            if _logging: rgb(f"\nAnalysing colors according to palette color: {paletteColor}", paletteColor[0], paletteColor[1], paletteColor[2])
            
            bestResult = {"similarity": -1.0, "color": (-1, -1, -1)}
            for apiColor in apiColors.values():
                similarity = utils.getColorsSimilarity(paletteColor, apiColor)
                print(f"analysing {apiColor}: {similarity}")
                
                if similarity > bestResult["similarity"]:
                    bestResult = {"similarity": similarity, "color": tuple(apiColor)}
            
            bestColor = bestResult["color"]
            
            # check if suited api color is grayscale
            if utils.isColorGrayscale(bestColor):
                print("Color is grayscale")
                continue
            else:
                return bestColor