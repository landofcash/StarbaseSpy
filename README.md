# StarbaseSpy
## Installation
- Install python 3.9 
- Download StarbaseSpy repo from git
- in the local StarbaseSpy folder in console run: 
  - python -m ensurepip
  - pip install -r requirements.txt
  - mkdir img
  - ren config.template.py config.py
- run the game, make sure game window name is "starbase" if not fix the name in fig.py
- in game open social menu O hotkey. 
- in the StarbaseSpy folder in console run
  - python main.py
 
 The script will create screenshots in the img folder. Make sure that 1.png looks ok and cut-before.png contain names from the list. (if not fix the left & top margins in the config.py)
 
 
 The script will compare two screenshots and Alarm (with sound) if there are changes. 
 The game window must NOT be minimized. 
