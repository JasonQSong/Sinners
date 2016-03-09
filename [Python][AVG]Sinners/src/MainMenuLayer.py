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
buttons=pygame.sprite.OrderedUpdates()

def startNewGame():
    pass
def loadGame():
    pass
def showGallery():
    pass
def close():
    pass

startbutton=None
def updateStartButton():
    global settings,startbutton
    startbutton.setPic(load_image("mainmenubutton_trans.png",-1))
    startbutton.setOnPic(load_image("mainmenubutton_on.png",-1))
    startbutton.setPos(560,370)
def startbutton_click(sender,event):
    startNewGame()

loadbutton=None
def updateLoadButton():
    global settings,loadbutton
    loadbutton.setPic(load_image("mainmenubutton_trans.png",-1))
    loadbutton.setOnPic(load_image("mainmenubutton_on.png",-1))
    loadbutton.setPos(560,420)
def loadbutton_click(sender,event):
    loadGame()

gallerybutton=None
def updateGalleryButton():
    global settings,gallerybutton
    gallerybutton.setPic(load_image("mainmenubutton_trans.png",-1))
    gallerybutton.setOnPic(load_image("mainmenubutton_on.png",-1))
    gallerybutton.setPos(560,470)
def gallerybutton_click(sender,event):
    showGallery()

exitbutton=None
def updateExitButton():
    global settings,exitbutton
    exitbutton.setPic(load_image("mainmenubutton_trans.png",-1))
    exitbutton.setOnPic(load_image("mainmenubutton_on.png",-1))
    exitbutton.setPos(560,520)
def exitbutton_click(sender,event):
    close()

def showMainMenuButtons():
    global buttons
    buttons.empty()
    global startbutton,loadbutton,gallerybutton,exitbutton
    buttons.add(startbutton)
    buttons.add(loadbutton)
    buttons.add(gallerybutton)
    buttons.add(exitbutton)
    
def init_MainMenuButtons():
    global startbutton
    startbutton=Button()
    startbutton.run=startbutton_click
    updateStartButton()
    global loadbutton
    loadbutton=Button()
    loadbutton.run=loadbutton_click
    updateLoadButton()
    global gallerybutton
    gallerybutton=Button()
    gallerybutton.run=gallerybutton_click
    updateGalleryButton()
    global exitbutton
    exitbutton=Button()
    exitbutton.run=exitbutton_click
    updateExitButton()
    
def init():
    global screen
    screen=pygame.display.get_surface()
    init_MainMenuButtons()

def show():
    global Closed
    Closed=False
    avgex.clearfg()
    avgex.setbg("title.jpg")
    avgex.playbgm("love song.mp3",20.20)
    showMainMenuButtons()
    
def remove():
    global Closed
    Closed=True
    global buttons
    buttons.empty()
    global startbutton,loadbutton,gallerybutton,exitbutton
    startbutton=None
    loadbutton=None
    gallerybutton=None
    exitbutton=None

def eventHandler(event):
    global buttons,onbutton
    if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_s:
        startNewGame()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_DOWN:
        tmplist=buttons.sprites()
        if onbutton==None:
            onbutton=tmplist[0]
        else:
            onbutton.setFocus(False)
            index=tmplist.index(onbutton)+1
            if index==len(tmplist):
                index=0
            onbutton=tmplist[index]
        onbutton.setFocus(True)
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_UP:
        tmplist=buttons.sprites()
        if onbutton==None:
            onbutton=tmplist[0]
        else:
            onbutton.setFocus(False)
            index=tmplist.index(onbutton)-1
            if index==len(tmplist):
                index=0
            onbutton=tmplist[index]
        onbutton.setFocus(True)
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_RETURN and event.mod == 4096:
        if onbutton!=None:
            onbutton.run(onbutton,event)
            return True
    elif event.type == pygame.locals.MOUSEBUTTONDOWN:
        mouse=pygame.mouse.get_pos()
        for tmpbtn in buttons:
            if tmpbtn.check(mouse):
                tmpbtn.run(tmpbtn,event)
        return True
    elif event.type == pygame.locals.MOUSEMOTION:
        onbutton=None
        mouse=pygame.mouse.get_pos()
        for tmpbtn in buttons:
            tmpon=tmpbtn.setMouse(mouse)
            if tmpon:
                onbutton=tmpbtn
    return False

def afterHandle():
    global screen,buttons
    global startbutton,loadbutton,gallerybutton,exitbutton
    buttons.update()
    buttons.draw(screen)
