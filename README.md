# Flagrate RGB
 Python app for users that want to add some ambiance to their workplace

# Structure
 This project consists of 2 parts: local-side (Python) and microcontroller-side (Arduino).

# Local-side
 Logins to user's Spotify account to collect user's current playing track. If any detected, extracts album's cover image most vibrant color to display on user's RGB light source.
 You're probably looking for this part if you want to reuse it.

# Microcontroller-side
 **Highly narrowly focused and dependent on the RGB light source and microcontroller.**

 Uses "IRremote.h" Arduino library to send IR commands to the RGB light source (RGB LED strip in my case). Receives commands sent via serial communication from the local-side. Requires IR LED to work.
 You should probably customize this part for your case.

# Roadmap
- [ ] **Some sort of caching** to reduce API requests and processing
- [ ] **Correcting support** for cases when main color is extracted from incorrectly or you have another view of it
- [ ] **Realtime color change accrodingly to display** for videogames, films, etc.
