from colorist import rgb, hsl as hls
from Pylette import extract_colors
from chromato import convert



class Color:
    """
    Color class
    
    Parameters
    ----------
    r : int
        Red color value (0-255)
    g : int
        Green color value (0-255)
    b : int
        Blue color value (0-255)
    """
    
    WHITE = (255, 255, 255)
    MAX_RGB_SINGLE = 255
    MAX_RGB_TOTAL = 255 * 3
    MAX_HUE = 360
    MAX_LIGHTNESS = 100
    MAX_SATURATION = 100
    
    def __init__(self, r: int, g: int, b: int) -> None:
        self._r = r
        self._g = g
        self._b = b
        
        self._h = None
        self._l = None
        self._s = None
    
    @property
    def r(self) -> int:
        """
        Red RGB color value (0-255)
        """
        return self._r
    
    @property
    def g(self) -> int:
        """Green RGB color value (0-255)"""
        return self._g
    
    @property
    def b(self) -> int:
        """Blue RGB color value (0-255)"""
        return self._b
        
    @property
    def rgb(self) -> tuple[int, int, int]:
        """Tuple of RGB color values"""
        return (self._r, self._g, self._b)
    
    def _rgb2hls(self):
        """Convert self to HLS color space and write the results to properties"""
        
        hsl_space = convert.rgb_to_hsl(self.rgb)
        
        self._h = int(hsl_space.h * Color.MAX_HUE)
        self._l = int(hsl_space.l * Color.MAX_LIGHTNESS)
        self._s = int(hsl_space.s * Color.MAX_SATURATION)
        
    @property
    def h(self) -> int:
        """HLS hue value (0-360)"""
        
        if not self._h:
            self._rgb2hls()
        
        return self._h
    
    @property
    def l(self) -> int:
        """HLS lightness value (0-100)"""
        
        if not self._l:
            self._rgb2hls()
        
        return self._l
    
    @property
    def s(self) -> int:
        """HLS saturation value (0-100)"""
        
        if not self._s:
            self._rgb2hls()
        
        return self._s

    @property
    def hls(self) -> tuple[int, int, int]:
        """Tuple of HLS color values"""
        
        if not self._h:
            self._rgb2hls()
        
        return (self._h, self._l, self._s)
    
    @property
    def is_grayscale(self) -> bool:
        """Check if the color is on grayscale range"""
        
        TOLERANCE = 7
        BLACK_WHITE_THRESHOLD = 34
        
        avg = (self._r + self._g + self._b) / 3
        
        # not in colorful range
        if not BLACK_WHITE_THRESHOLD < avg < (Color.MAX_RGB_SINGLE - BLACK_WHITE_THRESHOLD):
            return True
        
        # check if all color values are within the tolerance range of the average
        return all(abs(avg - channel) <= TOLERANCE for channel in self.rgb)
    
        # stub for hls check
        # palette_hls = rgb2hls(color) 
        # if palette_hls[1] < 15 or palette_hls[1] > 85: # too dark ot too bright
        #     msg = "too dark or too bright"
        #     vibrant_palette.remove(color)
        # elif palette_hls[2] < 20: # too unvibrant
        #     msg = "too unvibrant"
        #     vibrant_palette.remove(color)
        # else:
        #     msg = "appropriate"
            
        # if _logging: hls(f"{palette_hls} - {msg}", palette_hls[0], palette_hls[1], palette_hls[2])  
        
    def led_code(self, _logging: bool = False) -> tuple:
        """
        Get nearest color code from colors available in RGB LED.

        Note
        ----
        This is highly narrow solution. You would probably need to do it yourself accordinly to your RGB light source. In my case, it is an RGB LED strip with 16 colors available (5 R, G, and B tones each + white).

        Parameters
        ---------
        _logging : bool
            Whether to print advanced debug messages (default: False)

        Returns
        -------
        int, Color : color code in my case and the color itself
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
            311: 19,
            360: 4
        } # hue: code
        
        if _logging:
            colorful_output(f"Converted to HLS: {self.hls}", color=self, hls_mode=True) # type: ignore
            
        best_hue  = min(LED_COLOR_CODES.keys(), key=lambda led_hue: abs(led_hue - self.h))
        
        led_color = convert.hsl_to_rgb(best_hue / Color.MAX_HUE, 1, 0.5)
        led_color = Color(led_color.r, led_color.g, led_color.b)

        return LED_COLOR_CODES[best_hue], led_color

def colorful_output(text: str, color: Color, hls_mode: bool = False):
    """
    Print colored text to the console using `colorist`
    
    Parameters
    ----------
    text : str
        Text to be printed
    color : Color
        Color to be used
    hls_mode : bool
        Whether to use `hls` function (default: False)
    """
    
    if hls_mode:
        hls(text, color.h, color.l, color.s)
    else:
        rgb(text, color.r, color.g, color.b)

def get_colors_similarity(color1: Color, color2: Color) -> float:
    """
    Get similarity between two colors.

    Parameters
    ----------
    color1 : Color
    color2 : Color

    Returns
    -------
    float : similarity between two colors in normalized range [0, 1]
    """
    
    diff = (
        abs(color1.r - color2.r)
        + abs(color1.g - color2.g)
        + abs(color1.b - color2.b)
    )
    similarity = (Color.MAX_RGB_TOTAL - diff) / Color.MAX_RGB_TOTAL

    return similarity

def extract_main_color(image_url: str, _logging: bool = False) -> Color:
    """
    Extract most vibrant color from Spotify album cover image

    Parameters
    ----------
    image_url : str
        URL of image to extract the main color from 

    _logging : bool
        Whether to print advanced debug messages (default: False)

    Returns
    -------
    Color : main color extracted from image

    Note
    ----
    This function is suited for displaying color on RGB LED. Thus, vibrant colors are meant to be further exagerrated because dark colors on RGB LED look poor (for example, to display brown, you have to dim the orange). For the same reason any grayscale colors are displayed as white.
    """
    
    
    # extract main 5 colors palette from smaller image
    palette = extract_colors(image=image_url, palette_size=5).colors
    vibrant_palette = [] # here will be colors suitable for further processing
    
    if _logging: print("Colors extracted for grayscale check (RGB):")
    
    for palette_color in palette:
        palette_color = Color(*palette_color.rgb)
        
        if _logging: colorful_output(f"{palette_color.rgb}", palette_color)
        
        # check if each color is grayscale
        if palette_color.is_grayscale:
            if _logging: print("Grayscale")
        else:
            vibrant_palette.append(palette_color)
            if _logging: print("Not grayscale")
    
    # if the list is empty, the image is grayscale
    if not vibrant_palette:
        if _logging: print("The image is grayscale")
        return Color.WHITE
        
    if _logging:
        print("\nFinal colors:")
        for color in vibrant_palette:
            colorful_output(f"{color.rgb}", color)

    # return most dominant color
    return vibrant_palette[0]
