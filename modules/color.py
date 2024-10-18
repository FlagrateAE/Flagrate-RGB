from colorist import rgb, hsl as hls
from Pylette import extract_colors
from chromato import convert

class Color:
    """
    Color class
    
    Parameters
    ----------
    color : tuple[int, int, int]
        RGB color values: (r, g, b)
    """
    
    def __init__(self, color: tuple[int, int, int]) -> None:
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]


def is_color_grayscale(
    color: Color | tuple[int, int, int], tolerance: int = 7, black_white_threshold: int = 34) -> bool:
    """
    Check if a color is in the black-white range (grayscale).

    Parameters
    ----------
    color : tuple [int, int, int]
        RGB color values
    tolerance : int
        Maximum allowed difference between color channels (default: 7. This is an experimentally chosen value)
    black_white_threshold : int
        When color is considered too dark or too bright thus reverting to grayscale (default: 34. This is an experimentally chosen value)

    Returns
    -------
    bool : True if the color is grayscale, False otherwise
    """
    if isinstance(color, tuple):
        r = color[0]
        g = color[1]
        b = color[2]
    else:
        r = color.r
        g = color.g
        b = color.b

    # Calculate the average of the RGB values
    avg = (r + g + b) / 3

    if avg < black_white_threshold or avg > (255 - black_white_threshold):
        return True

    # Check if all color values are within the tolerance range of the average
    return all(abs(color - avg) <= tolerance for color in (r, g, b))


def rgb2hls(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Convert RGB color to HSL color.

    Parameters
    ----------
    color : tuple[int, int, int]
        RGB color values: R (0-255), G (0-255), B (0-255)

    Returns
    -------
    tuple[int, int, int]
        HSL color values: Hue (0-360), Lightness (0-100), Saturation (0-100)
    """
    result = convert.rgb_to_hsl(color)
    hue = int(result.h * 360)
    lightness = int(result.l * 100)
    saturation = int(result.s * 100)

    return hue, lightness, saturation

def get_colors_similarity(
    color1: tuple[int, int, int], color2: tuple[int, int, int]
) -> float:
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

    max_points = 255 * 3
    diff = (
        abs(color1[0] - color2[0])
        + abs(color1[1] - color2[1])
        + abs(color1[2] - color2[2])
    )
    similarity = (max_points - diff) / max_points

    return similarity

def extract_main_color(image_url: str, _logging: bool = False) -> tuple[int, int, int]:
    """
    Extract most vibrant color from Spotify album cover image

    Parameters
    ----------
    input : str
        URL of image to extract the main color from 

    _logging : bool
        Whether to print advanced debug messages (default: False)

    Returns
    -------
    tuple : (R, G, B)

    Note
    ----
    This function is suited for displaying color on RGB LED. Thus, vibrant colors are meant to be further exagerrated because dark colors on RGB LED look poor (for example, to display brown, you have to dim the orange). For the same reason any grayscale colors are displayed as white.
    """
    
    
    # extract main 5 colors palette from smaller image
    palette = extract_colors(image=image_url, palette_size=5).colors
    vibrant_palette = [] # here will be colors suitable for further processing
    
    if _logging: print("Colors extracted for grayscale check (RGB):")
    
    for palette_color in palette:
        palette_rgb = tuple(palette_color.rgb)
        if _logging: rgb(f"{palette_rgb}", palette_rgb[0], palette_rgb[1], palette_rgb[2])
        
        # check if each color is grayscale
        if is_color_grayscale(palette_rgb):
            if _logging: print("Grayscale")
        else:
            vibrant_palette.append(palette_rgb)
            if _logging: print("Not grayscale")
    
    # proceed with HLS threshold analysis
    if not vibrant_palette:
        if _logging: print("The image is grayscale")
        return (255, 255, 255)
    else:
        if _logging: print("\nHLS threshold analysis:")
        
    for color in vibrant_palette.copy():
        palette_hls = rgb2hls(color)
        
        if palette_hls[1] < 15 or palette_hls[1] > 85: # too dark ot too bright
            msg = "too dark or too bright"
            vibrant_palette.remove(color)
        elif palette_hls[2] < 20: # too unvibrant
            msg = "too unvibrant"
            vibrant_palette.remove(color)
        else:
            msg = "appropriate"
            
        if _logging: hls(f"{palette_hls} - {msg}", palette_hls[0], palette_hls[1], palette_hls[2])
    
    if not vibrant_palette:
        return (255, 255, 255)
        
    if _logging:
        print("\nFinal colors:")
        for color in vibrant_palette:
            rgb(f"{color}", color[0], color[1], color[2])

    # return most dominant color
    return vibrant_palette[0]