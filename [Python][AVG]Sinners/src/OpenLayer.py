# -*- coding: utf-8 -*-
import Layer
from Layer import *
#import pygame
import pygame
pygame.init()
#import pylib
import threading
#import userlib
from avgbase import *
import settings
import saveload
import lib_avgextend as avgex
import lib_font
from lib_font import Font
import lib_img
from lib_img import load_image
from lib_ui import *
Closed=True
screen=None
buttons=pygame.sprite.Group()

def BackToMenu():
    pass
  
def init():
    global screen
    screen=pygame.display.get_surface()

step=0
def show():
    global Closed,step
    Closed=False
    step=0
    nextstep()
    
def nextstep():
    global step
    if step==0:
        avgex.setbg("openning.png")
    elif step==1:
        avgex.setbg("openning.png")
    elif step==2:
        avgex.setbg("black.jpg")
    elif step==3:
        BackToMenu()
    step+=1

def remove():
    global Closed
    Closed=True
    
def eventHandler(event):
    return False

def afterHandle():
    if not settings.wait:
        nextstep()
