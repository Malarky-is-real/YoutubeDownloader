from ast import Num
from logging import root
from msilib.schema import CheckBox
from multiprocessing.spawn import import_main_path
from re import I
from statistics import variance
from tkinter import Tk
from typing import overload
from unicodedata import name
import eyed3
from eyed3.id3.frames import ImageFrame
import requests
import shutil
import os
from pytube import * 
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import DISABLED, Widget, ttk, Grid
import random as rand
import queue
import threading
import time 
from tkinter.scrolledtext import ScrolledText


songTitleFinal = ["bruh", "zone", "I", "hate", "money", "Jk", "I", "Love", "Money"]
main = tk.Tk()
main.geometry(f"100x100")

vid = Playlist(input("input file type :"))
for i in vid.videos: 
    print(i)
vid1r = vid[0]
print(type(vid1r))
vid1 = str(vid[0])
print(type(vid1))
print("[{0}]".format(', '.join(map(str, vid))))



main.mainloop()