from ast import Num
from multiprocessing.spawn import import_main_path
from re import I
from statistics import variance
from tkinter import Tk
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

def numcheck():
    global i
    tempi = rand.randint(1,2)
    print("tempi:", tempi)
    print("i in var:", i)

    while tempi == i:
        tempi = rand.randint(0,1)
        print("Random number is :", tempi)
    i = tempi
    print("tempi is ", tempi, " i is ", i)
    
i = 0
numcheck()
print("i:", i)
numcheck()
print("i:", i)