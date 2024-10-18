from colorist import rgb, hsl as hls
from Pylette import extract_colors

import modules.utils as utils


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
        if utils.is_color_grayscale(palette_rgb):
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
        palette_hls = utils.rgb2hls(color)
        
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