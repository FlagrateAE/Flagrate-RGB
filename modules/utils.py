from colorist import hsl as hls
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

    def hls(self) -> tuple[int, int, int]:
        pass


def clamp(val: int, minVal: int, maxVal: int) -> int:
    return max(min(val, maxVal), minVal)


def is_color_grayscale(
    color: Color | tuple[int, int, int], tolerance: int = 7, black_white_threshold: int = 34
) -> bool:
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
    hue = clamp(int(result.h * 360), 0, 360)
    lightness = clamp(int(result.l * 100), 0, 100)
    saturation = clamp(int(result.s * 100), 0, 100)

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


def get_nearest_color_code(color: tuple[int, int, int], _logging: bool = False) -> tuple:
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
    int, tuple[int, int, int] : Color code in my case and RGB values (0-255) of best mathcing color
    """
    LED_COLOR_CODES = {
        0: 4,
        41: 5,
        80: 6,
        90: 7,
        100: 8,
        120: 9,
        167: 10,
        177: 11,
        199: 13,
        205: 14,
        240: 15,
        252: 16,
        264: 17,
        274: 18,
        285: 19,
        360: 4
    } # hue: code
    
    color_hls = rgb2hls(color)
    
    if _logging:
        hls(f"Converted to HLS: {color_hls}", color_hls[0], color_hls[1], color_hls[2])
        
    best_hue  = min(LED_COLOR_CODES.keys(), key=lambda x: abs(x - color_hls[0]))
    
    color_rgb = convert.hsl_to_rgb(best_hue/360, 1, 0.5)
    color = color_rgb.r, color_rgb.g, color_rgb.b

    return LED_COLOR_CODES[best_hue], color