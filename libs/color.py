import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from colorsys import rgb_to_hls
from Pylette import extract_colors
from colorist import hsl, rgb

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
        
        
    def _isColorGrayscale(color: tuple[int, int, int], tolerance: int = 10) -> bool:
        """
        Check if a color is in the black-white range (grayscale).
        
        Args:
        r, g, b (int): RGB color values (0-255)
        tolerance (int): Maximum allowed difference between color channels (default: 10)
        
        Returns:
        bool: True if the color is grayscale, False otherwise
        """
        r, g, b = color[0], color[1], color[2]
        
        # Calculate the average of the RGB values
        avg = (r + g + b) / 3
        
        # Check if all color values are within the tolerance range of the average
        return all(abs(color - avg) <= tolerance for color in (r, g, b))
        
        
    def getCurrentPlayback(self) -> None | tuple[str, str, str, str, str]:
        """Get current playing track necessary information
        
        Returns
        -------
        If playback found\n
        tuple
            (albumName, albumID, imageURL, track, artist)
            
        If playback not found, None

        """
        result = self.client.current_playback()
        
        if not result:
            return None
        
        track = result['item']['name']
        artist = result['item']['artists'][0]['name']
        albumName = result['item']['album']['name']
        # albumID for dealing with non-ASCII named albums
        albumID = result['item']['album']['id']
        imageURL = result['item']['album']['images'][2]['url']
        
        return albumName, albumID, imageURL, track, artist
    
    def extractMainColor(self, imageURL: str) -> tuple[int, int, int]:
        """
        Extract most vibrant color from Spotify album cover image
        
        Parameters
        ----------
        imageURL : str
            Spotify album cover image URL in format "https://i.scdn.co/image/..."
            
        Returns
        -------
        tuple
            (R, G, B)
            
        Note
        ----
        This function is suited for displaying color on RGB LED. Thus, vibrant colors are further exagerrated because dark colors on RGB LED look poor (for example, to display brown, you have to dim the orange). Also for the same reason any grayscale colors are displayed as white.
        """
        
        # check for relatively grayscale image. for this, extract main 3 colors palette.  
        palette = extract_colors(image=requests.get(url=imageURL).content, palette_size=3)
        for c in palette.colors:
            crgb = c.rgb
            rgb(crgb, crgb[0], crgb[1], crgb[2])
            
            chsl = rgb_to_hls(crgb[0]/255, crgb[1]/255, crgb[2]/255)
            hsl(f"{chsl[0]*360:.2f} {chsl[2]*100:.2f} {chsl[1]*100:.2f}", chsl[0]*360, chsl[1]*100, chsl[2]*100)
        
        imageID = imageURL.split("/")[-1]
        
        colors: dict = requests.get(
            url="https://flagrate-vibrant-api.vercel.app?icon_id=" + imageID,
            headers={'Accept': 'application/json'}).json()
        
        # print(colors)
        # check

        
        # # if muted color has HSL saturation <= 10% (on grayscale), use white
        # # else use vibrant color
        # vibrantColorRGB = tuple(colors['vibrant'])
        
        # mutedColorRGB = colors['muted']
        # mutedSaturation = rgb_to_hls(
        #     mutedColorRGB[0]/255,
        #     mutedColorRGB[1]/255,
        #     mutedColorRGB[2]/255
        # )[2]
        
        # if mutedSaturation <= 0.1:
        #     return (255, 255, 255)
        # else:
        #     return vibrantColorRGB
        
        return colors
