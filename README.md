

<h1 align="center" style="font-weight: bold;">Flagrate RGB 💻</h1>


<p align="center">Python + Arduino project for the ones that want to add some color to their workplace</p>



<h2 id="technologies">💻 Technologies</h2>

- Python
- C++ (Arduino)
- IR communication (NEC protocol)

<h2>🎨 Features</h2>

- Spotify playback monitoring
- Color extraction from album cover image
- Tray control interface
- Local-only mode + advanced logging mode (see [Starting](#commands))

<h2 id="started">🚀 Getting started</h2>

This project consists of 2 parts: local-side (Python) and microcontroller-side (Arduino)

#### Local-side 
Logins to user's Spotify account to collect user's current playing track. If any detected, extracts album's cover image most vibrant color with complex algorithm to display on user's RGB light source.

<b>You're probably looking for this part if you want to reuse it.</b>

#### Microcontroller-side
Highly narrowly focused and dependent on the RGB light source and microcontroller.

Uses "IRremote.h" Arduino library to send IR commands to the RGB light source (RGB LED strip in my case). Receives commands sent via serial communication from the local-side. Requires IR LED to work. 

<b>You should probably customize this part for your case.</b>

<h3>Prerequisites</h3>

Here you list all prerequisites necessary for running your project. For example:

- [Python 3.10.11](https://python.org)
- [Arduino IDE 2 (optional)](https://www.arduino.cc/en/software)
- Git + GitHub

<h3>Installation</h3>

Clone the repository and install the dependencies

```bash
git clone https://github.com/FlagrateAE/Flagrate-RGB
cd Flagrate-RGB
pip install -r requirements.txt
```

<h3>Starting</h3>
Make sure to configure the following three environment variables:
    
    SPOTIFY_CLIENT_ID
    
    SPOTIFY_CLIENT_SECRET
    
    SPOTIFY_REDIRECT_URI

For further details, see [official Spotify documentation](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow)<br><br>

```bash
python3 main.py
```

<h4 id = "commands">Attention!</h4>
The above command runs the program at the default state. It accepts command line arguments:

<br>

```bash
python3 main.py --local-only
```
Runs only color-extracting part (local-side). Great for your testing if you have (no doubt) a setup different from mine
<br>
<br>


```bash
python3 main.py --log
```
Enables advanced log messages. Useful for debugging and seeing how it works under the hood