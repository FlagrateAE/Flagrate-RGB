import pystray
from PIL import Image, ImageDraw
from time import sleep
from modules.utils import Playback


class Tray(pystray.Icon):
    def __init__(self) -> None:
        """
        Start program tray icon loop.
        """

        super().__init__(
            name="flagratergb",
            title="Flagrate RGB",
            menu=self.menu_generator(track=None, artist=None, album=None),
            icon=Image.open("modules/drawable/icon.png"),
        )
        self.f_running = True
        self.run_detached()

    def f_stop(self) -> None:
        """
        Stop the entire program.
        """

        self.f_running = False
        self.stop()

    def menu_generator(self, track: str, artist: str, album: str) -> pystray.Menu:
        """
        Generate tray icon menu that pops up on RMB click accrodingly to current system state.

        Parameters
        ----------
        track : str
            Current track name
        artist : str
            Current artist name
        album : str
            Current album name

        If no music is playing, pass any of these as None.
        """

        if not track or not artist or not album:
            return pystray.Menu(
                pystray.MenuItem(
                    text="⏸️ No playback",
                    action=None,
                ),
                pystray.MenuItem(text="⛔ Stop", action=self.f_stop),
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
                pystray.MenuItem(text="⛔ Stop", action=self.f_stop),
            )

    def display_color(self, color: tuple[int, int, int], show_spotify_icon: bool = False):
        """
        Set tray icon color.

        Parameters
        ----------
        color : tuple[int, int, int]
            RGB color values: (r, g, b)
        show_spotify_icon : bool
            Whether to draw Spotify icon (default: False)
        """
        new_icon = Image.new("RGBA", (42, 42))
        draw = ImageDraw.Draw(new_icon)

        # outer white
        draw.ellipse([(0, 0), (40, 40)], fill="white")
        # inner black
        draw.ellipse([(2, 2), (38, 38)], fill="black")
        # display desired color
        draw.ellipse([(4, 4), (36, 36)], fill=color)

        if show_spotify_icon:
            new_icon = Image.alpha_composite(
                im1=new_icon,
                im2=Image.open("modules/drawable/spotify.png").resize((42, 42)),
            )

            # wait to load
            sleep(0.05)

        self.icon = new_icon

    def spotify(self, playback: Playback, color: tuple[int, int, int]):
        """
        Set playing track info to be displayed in tray icon menu.

        Parameters
        ----------
        playback : Playback
            Current Spotify playback (class in utils.py)
        color : tuple[int, int, int]
            RGB color values: (r, g, b)
        """

        self.menu = self.menu_generator(
            playback.track, playback.artist, playback.album_name
        )
        self.display_color(color=color, show_spotify_icon=True)
