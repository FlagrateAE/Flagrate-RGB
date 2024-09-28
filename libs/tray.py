import pystray
from PIL import Image, ImageDraw
from random import randint
from time import sleep
from os import getcwd

class Tray(pystray.Icon):
    fRunning = False
    def _fStop(self):
        self.fRunning = False
        self.stop()
            
    def _menuGenerator(self, track: str, artist: str, album: str):
        if not track:
            return pystray.Menu(
                        pystray.MenuItem(
                            text="⏸️ Воспроизведения нет",
                            action=None,
                        ),
                        pystray.MenuItem(
                            text="⛔ Завершить",
                            action=self._fStop
                        )
                     )
        else:
            return pystray.Menu(
                        pystray.MenuItem(
                            text=f"🎧 {artist} - {track}",
                            action=None,
                        ),
                        pystray.MenuItem(
                            text=f"📀 {album}",
                            action=None,
                        ),
                        pystray.MenuItem(
                            text="⛔ Завершить",
                            action=self._fStop
                        )
            )
            
    def __init__(self):
        
        icon = super().__init__(
            name="flagratergb",
            title="Flagrate RGB",
            menu=self._menuGenerator(track=None, artist=None, album=None),
            icon=Image.open("libs/drawable/icon.ico")
        )
        self.fRunning = True
        self.run_detached()
        
    def spotify(self, track: str, artist: str, album: str):
        """
        Установить состояние проигрывателя Spotify
        """
        
        self.menu = self._menuGenerator(track, artist, album)
        
    def displayColor(self, r: int, g: int, b: int):
        """
        Вывести цвет системы
        """
        newIcon = Image.new('RGBA', (42, 42))
        draw = ImageDraw.Draw(newIcon)
        
        # outer white
        draw.ellipse([(0, 0), (40, 40)], fill='white')
        # inner black
        draw.ellipse([(2, 2), (38, 38)], fill='black')
        # display desired color
        draw.ellipse([(4, 4), (36, 36)], fill=(r, g, b))            
        
        newIcon = Image.alpha_composite(
            im1=newIcon,
            im2=Image.open("libs/drawable/spotify.png").resize((42, 42)),
        )
        
        # wait to load
        sleep(0.05)
        
        self.icon = newIcon
        