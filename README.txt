 _____                             _       ___  ______                     _        
/  __ \                           | |     /   | | ___ \                   | |       
| /  \/ ___  _ __  _ __   ___  ___| |_   / /| | | |_/ /_ _ _ __   ___ __ _| | _____ 
| |    / _ \| '_ \| '_ \ / _ \/ __| __| / /_| | |  __/ _` | '_ \ / __/ _` | |/ / _ \
| \__/\ (_) | | | | | | |  __/ (__| |_  \___  | | | | (_| | | | | (_| (_| |   <  __/
 \____/\___/|_| |_|_| |_|\___|\___|\__|     |_/ \_|  \__,_|_| |_|\___\__,_|_|\_\___|
                                                                                    
A spin on Connect 4 :)
=====================================================================================

https://jhan1.itch.io/connect-4-pancake

Play a game of Connect 4 at this lovely pancake cafe, with a fun new twist!
Rotate the board to create new strategies to out-connect your opponents!

Made by "257 Korea" in August 2020 for UniJam 2020 (https://unijam.org.au/),
a week-long game development hackathon at the University of Melbourne.

Jonathan Jauhari
Jun Hee Han
Sooyoung Jung
Tianchen Lou

---------------------------
Running the executable
---------------------------

in 'releases'

Windows 10:

.\exe.win-amd64-3.7\connect4pancake.exe

---------------------------
Running from source
---------------------------

Windows 10:

1. Ensure Python 3.7+ is installed
2. Run the following commands, in a virtual environment (conda/venv), or otherwise:

   pip install numpy
   pip install pygame
   pip install pygame_gui
   python connect4plus.py


Ubuntu 20.04:

1. Ensure Python 3.7+ is installed
2. Run (needs root access):
   
   sudo apt-install python3-pygame

3. Run the following commands, in a virtual environment (conda/venv), or otherwise:

   pip3 install numpy
   pip3 install pygame_gui
   python connect4plus.py


---------------------------
Acknowledgements
---------------------------
sound files:

- sound effects: https://freesound.org
- background music: https://www.bensound.com

image files:

- pancake: https://www.flaticon.com/free-icon/pancake_1256465
- teddy bear: https://www.flaticon.com/search/2?search-type=icons&word=teddy+bear


---------------------------
License
---------------------------

Copyright (c) 2020 "257 Korea"

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
