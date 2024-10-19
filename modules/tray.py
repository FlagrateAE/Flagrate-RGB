import pystray
from PIL import Image, ImageDraw
from time import sleep

from modules.color import Color


class Tray(pystray.Icon):
    def __init__(self) -> None:
        """
        Start program tray icon loop.
        """

        super().__init__(
            name="flagratergb",
            title="Flagrate RGB",
            menu=self.menu_generator(None),
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

    def menu_generator(self, playback: dict | None) -> pystray.Menu:
        """
        Generate tray icon menu that pops up on RMB click accrodingly to current system state.

        Parameters
        ----------
        playback : dict or None
            Current Spotify playback (see SpotifyRequestHandler.get_current_playback()) or None if no track is playing
        """

        if not playback:
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
                    text=f'🎧 {playback["artist"]} - {playback["track"]}',
                    action=None,
                ),
                pystray.MenuItem(
                    text=f'📀 {playback["album_name"]}',
                    action=None,
                ),
                pystray.MenuItem(text="⛔ Stop", action=self.f_stop),
            )

    def display_color(self, color: Color, show_spotify_icon: bool = False) -> None:
        """
        Set tray icon color.

        Parameters
        ----------
        color : Color
            Color to display in tray
        show_spotify_icon : bool
            Whether to draw Spotify icon (default: False)
        """
        
        ICON_LOAD_DELAY = 0.05
        
        new_icon = Image.new("RGBA", (42, 42))
        draw = ImageDraw.Draw(new_icon)

        # outer white
        draw.ellipse([(0, 0), (40, 40)], fill="white")
        # inner black
        draw.ellipse([(2, 2), (38, 38)], fill="black")
        # display desired color
        draw.ellipse([(4, 4), (36, 36)], fill=color.rgb)

        if show_spotify_icon:
            new_icon = Image.alpha_composite(
                im1=new_icon,
                im2=Image.open("modules/drawable/spotify.png").resize((42, 42)),
            )

            # wait to load
            sleep(ICON_LOAD_DELAY)

        self.icon = new_icon

    def display_spotify(self, playback: dict, color: Color) -> None:
        """
        Set playing track info to be displayed in tray icon menu.

        Parameters
        ----------
        playback : dict
            Current Spotify playback (see SpotifyRequestHandler.get_current_playback())
        color : Color
            Color to display in tray
        """

        self.menu = self.menu_generator(playback)
        self.display_color(color, show_spotify_icon=True)

