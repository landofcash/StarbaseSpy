# StarbaseSpy
## Installation
- Install python 3.9 
- Pull StarbaseSpy repo from git
- in the local StarbaseSpy folder in console (CMD) run: 
  - python -m ensurepip
  - pip install -r requirements.txt
  - mkdir img
  - ren config.template.py config.py
- run the game, make sure game window name is "starbase" if not fix the name in config.py
- in game open social menu O hotkey. 
- in the StarbaseSpy folder in console run
  - python main.py
 
 The script will create screenshots in the img folder. Make sure that 1.png looks ok and contain names from the list. (if not fix the left & top margins in the config.py)
 
 
 The script will compare two screenshots and Alarm (with sound) if there are changes and send the image to FH discord bot. 
 The game window must NOT be minimized but can be overlapped with other windows. 
