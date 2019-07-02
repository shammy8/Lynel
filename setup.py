import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": ["pygame", "random", "sys", "pygame.sprite"],
                     "excludes": ['tkinter'],
                     "include_files": ["sounds/Palace.mp3","sounds/DarkGoldenLand.mp3","sounds/Classic.mp3",'images/heart.png','images/link.png',
                     'images/enemies.png','images/arrow2.png','images/mybombchu2.png','images/bomb_explode_big.png',"images/background1.png",]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Lynel Invasion",
      version="1.0",
      description="Flap around",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="game.py", base=base)])