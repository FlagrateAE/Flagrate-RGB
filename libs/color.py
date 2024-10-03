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
        
        
    def _isColorGrayscale(self, color, tolerance: int = 6.5) -> bool:
        """
        Check if a color is in the black-white range (grayscale).
        
        Parameters
        ----------
        color : tuple or list
            RGB color values (0-255)
        tolerance : int 
            Maximum allowed difference between color channels (default: 6. This is experimentally chosen value)
        
        Returns
        -------
        bool : True if the color is grayscale, False otherwise
        """
        r = color[0]
        g = color[1]
        b = color[2]
        
        # Calculate the average of the RGB values
        avg = (r + g + b) / 3
        
        # Check if all color values are within the tolerance range of the average
        return all(abs(color - avg) <= tolerance for color in (r, g, b))
        
    def _isImageGrayscale(self, imageURL: str, tolerance: int = 6.5, _logging: bool = False) -> bool:
        """
        Check if a image`s color palette is grayscale.
        
        Parameters
        ----------
        imageURL : str
            URL of examined image
        tolerance : int
            Maximum allowed difference between color channels (default: 6. This is experimentally chosen value)
        _logging : bool
            Whether to print advanced debug messages (default: False)
        
        Returns
        --------
        bool : True if the image is grayscale, False otherwise
        """
        
        image = requests.get(url=imageURL).content
        palette = extract_colors(image=image, palette_size=3)
        
        grayscalance = []
        
        if _logging:print("Palette extracted for grayscale detection:")
        
        for color in palette.colors:
            grayscalance.append(self._isColorGrayscale(color=color.rgb, tolerance=tolerance))
            
            if _logging:
                rgb(tuple(color.rgb), color.rgb[0], color.rgb[1], color.rgb[2])
                print("Grayscale") if grayscalance[-1] == True else print("Not grayscale")
                
        result = all(grayscalance)
        
        if _logging:
            print("The image is grayscale") if result == True else print("Image is colorful")
        
        return result
        
    def getCurrentPlayback(self) -> tuple[str, str, str, str, str] | None:
        """Get current playing track necessary information
        
        Parameters
        ----------
        _logging : bool
            Whether to print advanced debug messages (default: False)
        
        Returns
        -------
        tuple : (albumName, albumID, imageURL, track, artist)
        None : if no track is playing
        """
        
        result = self.client.current_playback()
        
        try:
            track = result['item']['name']
            artist = result['item']['artists'][0]['name']
            albumName = result['item']['album']['name']
            # albumID for dealing with non-ASCII named albums
            albumID = result['item']['album']['id']
            imageURL = result['item']['album']['images'][0]['url']
        except:
            return None
        
        return albumName, albumID, imageURL, track, artist
    
    
    def extractMainColor(self, imageURL: str, _logging: bool = False) -> tuple[int, int, int]:
        """
        Extract most vibrant color from Spotify album cover image
        
        Parameters
        ----------
        imageURL : str
            Spotify album cover image URL in format "https://i.scdn.co/image/..."
        _logging : bool
            Whether to print advanced debug messages (default: False)
            
        Returns
        -------
        tuple : (R, G, B)
            
        Note
        ----
        This function is suited for displaying color on RGB LED. Thus, vibrant colors are meant to be further exagerrated because dark colors on RGB LED look poor (for example, to display brown, you have to dim the orange). Also for the same reason any grayscale colors are displayed as white.
        """
        
        # check for relatively grayscale image. for this, extract main 3 colors palette. if so, return just white
        if self._isImageGrayscale(imageURL=imageURL, _logging=_logging):
            return (255, 255, 255)
        
        # if not grayscale, proceed with vibrant color from flagrate vibrant api
        imageID = imageURL.split("/")[-1]
        
        colors: dict = requests.get(
            url="https://flagrate-vibrant-api.vercel.app?icon_id=" + imageID,
            headers={'Accept': 'application/json'}).json()
        
        if _logging:
            for color in colors:
                rgb(f"{color}: {tuple(colors[color])}", colors[color][0], colors[color][1], colors[color][2])
        
        return tuple(colors["vibrant"])
