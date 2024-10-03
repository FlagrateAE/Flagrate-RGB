import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from colorist import rgb
import libs.utils as utils

class Playback:
    def __init__(self, currentPlayback: dict) -> None:
        """
        Contruct a Playback object from Spotify current playback
        
        Parameters
        ----------
        currentPlayback : dict
            Spotify current playback recieved from spotipy.Spotify.current_playback()
        """
        self.track:str = currentPlayback['item']['name']
        self.artist:str = currentPlayback['item']['artists'][0]['name']
        self.albumName:str = currentPlayback['item']['album']['name']
        # albumID for dealing with non-ASCII named albums
        self.albumID:str = currentPlayback['item']['album']['id']
        self.imageURL:str = currentPlayback['item']['album']['images'][0]['url']

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
        
        if utils.isImageGrayscale(imageURL=imageURL, _logging=_logging):
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
