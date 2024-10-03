import requests
from Pylette import extract_colors
from colorist import rgb

def isColorGrayscale(color: tuple[int, int, int], tolerance: int = 6.5) -> bool:
        """
        Check if a color is in the black-white range (grayscale).
        
        Parameters
        ----------
        color : tuple [int, int, int]
            RGB color values
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
    

def isImageGrayscale(imageURL: str, tolerance: int = 6.5, _logging: bool = False) -> bool:
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
            grayscalance.append(isColorGrayscale(color=color.rgb, tolerance=tolerance))
            
            if _logging:
                rgb(tuple(color.rgb), color.rgb[0], color.rgb[1], color.rgb[2])
                print("Grayscale") if grayscalance[-1] == True else print("Not grayscale")
                
        result = all(grayscalance)
        
        if _logging:
            print("The image is grayscale") if result == True else print("Image is colorful")
        
        return result
    
    
def getNearestColorCode(color: tuple[int, int, int]) -> tuple:
        """
        Get nearest color code from colors available in RGB LED.
        
        Note
        ----
        This is highly narrow solution. You would probably need to do it yourself accordinly to your RGB light source. In my case, it is an RGB LED strip with 16 colors available (5 R, G, and B tones each + white).
        
        Parameters
        ---------
        color : tuple[int, int, int]
            RGB color values: (r, g, b)
            
        Returns
        -------
        tuple : (int, tuple[int, int, int])
            Color code in my case and color RGB values
        """
        LED_COLOR_CODES = {
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
        
        bestResult = [-1, -1, (-1, -1, -1)] # [color code, similarity, color]
        maxPoints = 255 * 3
        for ledColor in LED_COLOR_CODES:
            diff = abs(ledColor[0] - color[0]) + abs(ledColor[1] - color[1]) + abs(ledColor[2] - color[2])
            
            similarity = (maxPoints - diff)/maxPoints
            
            if similarity > bestResult[1]:
                bestResult = [LED_COLOR_CODES[ledColor], similarity, ledColor]
        
        return bestResult[0], bestResult[2]