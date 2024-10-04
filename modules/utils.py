from colorist import rgb
from Pylette import Palette


class Playback:
    def __init__(self, currentPlayback: dict) -> None:
        """
        Construct a Playback object from Spotify current playback

        Parameters
        ----------
        currentPlayback : dict
            Spotify current playback recieved from spotipy.Spotify.current_playback()
        """
        self.track: str = currentPlayback["item"]["name"]
        self.artist: str = currentPlayback["item"]["artists"][0]["name"]

        self.albumName: str = currentPlayback["item"]["album"]["name"]
        # albumID for dealing with non-ASCII named albums
        self.albumID: str = currentPlayback["item"]["album"]["id"]

        self.bigImage: str = currentPlayback["item"]["album"]["images"][0]["url"]
        self.smallImage: str = currentPlayback["item"]["album"]["images"][2]["url"]


def isColorGrayscale(
    color: tuple[int, int, int], tolerance: int = 6.5, blackwhiteThreshold: int = 35
) -> bool:
    """
    Check if a color is in the black-white range (grayscale).

    Parameters
    ----------
    color : tuple [int, int, int]
        RGB color values
    tolerance : int
        Maximum allowed difference between color channels (default: 6. This is an experimentally chosen value)
    blackwhiteThreshold : int
        When color is considered too dark or too bright thus reverting to grayscale (default: 35. This is an experimentally chosen value)

    Returns
    -------
    bool : True if the color is grayscale, False otherwise
    """
    r = color[0]
    g = color[1]
    b = color[2]

    # Calculate the average of the RGB values
    avg = (r + g + b) / 3

    if avg < blackwhiteThreshold or avg > (255 - blackwhiteThreshold):
        return True

    # Check if all color values are within the tolerance range of the average
    return all(abs(color - avg) <= tolerance for color in (r, g, b))


def getImageGrayscalance(
    palette: Palette,
    tolerance: int = 6.5,
    _logging: bool = False,
) -> list[bool]:
    """
    Check if a image`s color palette is grayscale.

    Parameters
    ----------
    palette : Palette
        Pylette Palette object
    tolerance : int
        Maximum allowed difference between color channels (default: 6. This is experimentally chosen value)
    _logging : bool
        Whether to print advanced debug messages (default: False)

    Returns
    --------
    list[bool] : list of statements for is each color grayscale
    """

    grayscalance = []

    if _logging:
        print("Palette extracted for grayscale detection:")

    for color in palette.colors:
        grayscalance.append(isColorGrayscale(color=color.rgb, tolerance=tolerance))

        if _logging:
            rgb(tuple(color.rgb), color.rgb[0], color.rgb[1], color.rgb[2])
            print("Grayscale") if grayscalance[-1] == True else print("Not grayscale")

    return grayscalance

def getColorsSimilarity(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
    """
    Get similarity between two colors.

    Parameters
    ----------
    color1 : tuple[int, int, int]
        First RGB color values
    color2 : tuple[int, int, int]
        Second RGB color values

    Returns
    -------
    float : similarity between two colors in normalized range [0, 1]
    """
    
    maxPoints = 255*3
    diff = (
            abs(color1[0] - color2[0])
            + abs(color1[1] - color2[1])
            + abs(color1[2] - color2[2])
        )
    similarity = (maxPoints - diff) / maxPoints
    
    return similarity

def getNearestColorCode(color: tuple[int, int, int], _logging: bool = False) -> tuple:
    """
    Get nearest color code from colors available in RGB LED.

    Note
    ----
    This is highly narrow solution. You would probably need to do it yourself accordinly to your RGB light source. In my case, it is an RGB LED strip with 16 colors available (5 R, G, and B tones each + white).

    Parameters
    ---------
    color : tuple[int, int, int]
        RGB color values: (r, g, b)
    _logging : bool
        Whether to print advanced debug messages (default: False)

    Returns
    -------
    tuple : (int, tuple[int, int, int])
        Color code in my case and color RGB values
    """
    LED_COLOR_CODES = {
        (255, 0, 0): 4,
        (255, 175, 0): 5,
        (212, 255, 0): 6,
        (175, 255, 0): 7,
        (166, 255, 0): 8,
        (0, 255, 0): 9,
        (0, 255, 200): 10,
        (0, 255, 242): 11,
        # (255, 255, 255): 12,
        (0, 175, 255): 13,
        (0, 149, 255): 14,
        (0, 0, 255): 15,
        (50, 0, 255): 16,
        (100, 0, 255): 17,
        (145, 0, 255): 18,
        (190, 0, 255): 19,
    }
    
    if _logging: print("\nNow seeking among the available colors...")
    
    bestResult = {"code": -1, "similarity": -1.0, "color": (-1, -1, -1)}

    for ledColor in LED_COLOR_CODES:
        similarity = getColorsSimilarity(ledColor, color)

        if _logging: print(f"Analyzing {ledColor}: {similarity}")
        if similarity > bestResult["similarity"]:
            bestResult = {"code": LED_COLOR_CODES[ledColor], "similarity": similarity, "color": ledColor}

    return bestResult["code"], bestResult["color"]
