from serial import Serial
import time

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
        
        self._IR_COLOR_CODES = {
            (255,0,0): 4,
            (255,175,0): 5,
            (212,255,0): 6,
            (175,255,0): 7,
            (166,255,0): 8,
            (0,255,0): 9,
            (0,255,200): 10,
            (0,255,242): 11,
            (255,255,255): 12,
            (0,175,255): 13,
            (0,149,255): 14,
            (0,0,255): 15,
            (50,0,255): 16,
            (100,0,255): 17,
            (145,0,255): 18,
            (190,0,255): 19
        }
    
    def send(self, data: str):
        """Send text data to Arduino via serial
        
        Parameters
        ----------
        data : str
        Text data to be sent"""
        self.write(bytes(data, 'utf-8'))
    
    def receive(self):
        return self.readline()
    
    def _getNearestColorCode(self, color: tuple[int, int, int]) -> int:
        """
        Get nearest color code from colors available in RGB LED.
        
        Note
        ----
        This is highly narrow solution. You would probably need to do it yourself accordinly to your RGB light source. In my case, it is an RGB LED strip with 16 colors available (5 R, G, and B tones each + white).
        
        Parameters
        ---------
        color : tuple[int, int, int]
            RGB color values: (r, g, b)
        """
        
        bestResult = [-1, -1] # [color code, similarity]
        maxPoints = 255 * 3
        for color in self._IR_COLOR_CODES:
            diff = abs(color[0] - color[0]) + abs(color[1] - color[1]) + abs(color[2] - color[2])
            
            similarity = (maxPoints - diff)/maxPoints
            
            if similarity > bestResult[1]:
                bestResult = [self._IR_COLOR_CODES[color], similarity]
        
        return bestResult[0]