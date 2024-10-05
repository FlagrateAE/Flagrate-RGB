import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

from colorist import rgb
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
        self, playback: Playback, imageURL: str, _logging: bool = False
    ) -> tuple[int, int, int]:
        """
        Extract most vibrant color from Spotify album cover image

        Parameters
        ----------
        playback : Playback
            Spotify current playback
        imageURL : str
            For cases if you want to extract the main color outside of Spotify
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
            imageURL = playback.bigImage
        elif not imageURL:
            raise ValueError("No image URL provided")
        
        
        # extract main 6 colors palette from smaller image. if so, return just white
        palette = extract_colors(image=imageURL, palette_size=6)

        grayscalance = utils.getImageGrayscalance(palette=palette, _logging=_logging)
        if all(grayscalance):
            return (255, 255, 255)

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

        # get first not grayscale color from palette
        for i, paletteColor in enumerate(palette.colors):
            # if palette color is grayscale, proceed to next
            if grayscalance[i]: continue
            
            print("\nAnalyzing colors according to palette color:", paletteColor.rgb)
            bestResult = {"similarity": -1.0, "color": (-1, -1, -1)}
            for apiColor in apiColors.values():
                similarity = utils.getColorsSimilarity(paletteColor.rgb, apiColor)
                print(f"Analyzing {apiColor}: {similarity}")
                
                if similarity > bestResult["similarity"]:
                    bestResult = {"similarity": similarity, "color": tuple(apiColor)}
            
            bestColor = bestResult["color"]
            if utils.isColorGrayscale(bestColor):
                print("Color is grayscale")
                continue
            else:
                return bestColor