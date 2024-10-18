from serial import Serial
import time

from chromato import convert
from colorist import hsl as hls

from modules.color import rgb2hls

class Arduino(Serial):
    def __init__(self, port: str):
        """Initialize serial connection to Arduino
        
        Parameters
        ----------
        port : str
            Serial port name (COM* for Windows, /dev/tty* for Linux)
        """
        
        super().__init__(port=port, baudrate=9600, bytesize=8, parity="N", stopbits=1)
        
        time.sleep(2)
        print("Arduino connected")
    
    def send(self, data: str):
        """Send text data to Arduino via serial
        
        Parameters
        ----------
        data : str
        Text data to be sent"""
        self.write(bytes(data, 'utf-8'))
    
    def receive(self):
        """
        This funcion is a stub
        """
        return self.readline()
    
    
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
        310: 19,
        361: 4
    } # hue: code
    
    color_hls = rgb2hls(color)
    
    if _logging:
        hls(f"Converted to HLS: {color_hls}\n", color_hls[0], color_hls[1], color_hls[2])
        
    best_hue  = min(LED_COLOR_CODES.keys(), key=lambda x: abs(x - color_hls[0]))
    
    color_rgb = convert.hsl_to_rgb(best_hue/360, 1, 0.5)
    color = color_rgb.r, color_rgb.g, color_rgb.b

    return LED_COLOR_CODES[best_hue], color