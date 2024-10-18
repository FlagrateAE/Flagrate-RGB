import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyRequestHandler:
    """
    Executes Spotify API requests via `spotipy` lib
    
    Parameters
    ----------
    client_id : str
        Spotify client ID
    client_secret : str
        Spotify client secret
    redirect_uri : str
        Spotify redirect URI

    Those should be acquired from https://developer.spotify.com/dashboard
    """
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id, client_secret, redirect_uri,
                scope="user-read-currently-playing user-read-playback-state",
            )
        )

    def get_current_playback(self) -> dict | None:
        """
        Get current Spotify playback

        Returns
        -------
        dict : if track is playing
            Keys: "track", "artist", "album_name", "album_id", "image_url"
        None : if no track is playing or any error occurs
        """

        try:
            result = self.client.current_playback()
            
            playback = {
                "track": result["item"]["name"],
                "artist": result["item"]["artists"][0]["name"],
                "album_name": result["item"]["album"]["name"],
                "album_id": result["item"]["album"]["id"],
                "image_url": result["item"]["album"]["images"][0]["url"],
            }

            return playback
        
        except Exception as e:
            if not isinstance(e, TypeError): print(e) # TypeError is raised when no track is playing
            return None
