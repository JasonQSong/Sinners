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

story=None

class Game_Data:
    readdata=None
    gamedata=None
data=Game_Data()

def setcgindex(i):
    global story,nowcg,totcg,cgcollection
    settings.wait=True
    nowcg=i
    if i==0:
        avgex.setcg("black.jpg")
        cglabel.setTxt("%2d/%2d     %s"%(nowcg,totcg-1,cgcollection),(10,10))
        return None
    XEcg=story.XEcgs.getElementsByTagName("cg")[i]
    filename=XEcg.getAttribute("name")
    avgex.setcg(filename)
    cglabel.setTxt("%2d/%2d     %s"%(nowcg,totcg-1,cgcollection),(10,10))

def setbgmindex(i):
    global story,nowbgm,totbgm
    nowbgm=i
    XEbgm=story.XEbgms.getElementsByTagName("bgm")[i]
    filename=XEbgm.getAttribute("name")
    avgex.playbgm(filename)
    bgmlabel.setTxt("%2d/%2d   %s"%(nowbgm,totbgm-1,filename),(10,10))

def precg():
    if settings.wait:
        return None
    global data,nowcg,totcg
    index=nowcg-1
    while index>0:
        if data.readdata.cgs[index]:
            break
        index-=1
    if index<0:
        return None
    setcgindex(index)

def nextcg():
    if settings.wait:
        return None
    global data,nowcg,totcg
    index=nowcg+1
    while index<totcg:
        if data.readdata.cgs[index]:
            break
        index+=1
    if index>=totcg:
        return None
    setcgindex(index)
    
def prebgm():
    global data,nowbgm,totbgm
    index=nowbgm-1
    if index<=0:
        return None
    setbgmindex(index)

def nextbgm():
    global data,nowbgm,totbgm
    index=nowbgm+1
    if index>=totbgm:
        return None
    setbgmindex(index)

def changeOnlyPic():
    global settings
    if settings.onlypic:
        settings.onlypic=False
    else:
        settings.onlypic=True

menubutton=None
def updateMenuButton():
    global settings,memubutton
    menubutton.setPic(load_image("littlebutton_orange.png",-1))
    menubutton.setOnTxt("Menu",(10,5))
    menubutton.setPos(0,0)
def menubutton_click(sender,event):
    BackToMenu()
    
precgbutton=None
def updatePreCgButton():
    global precgbutton
    precgbutton.setPic(load_image("prebar.png",-1))
    precgbutton.setOnPic(load_image("prebar_orange.png",-1))
    precgbutton.setPos(140,0)
def precgbutton_click(sender,event):
    precg()

nextcgbutton=None
def updateNextCgButton():
    global nextcgbutton
    nextcgbutton.setPic(load_image("nextbar.png",-1))
    nextcgbutton.setOnPic(load_image("nextbar_orange.png",-1))
    nextcgbutton.setPos(610,0)
def nextcgbutton_click(sender,event):
    nextcg()
    
prebgmbutton=None
def updatePreBgmButton():
    global prebgmbutton
    prebgmbutton.setPic(load_image("prebar.png",-1))
    prebgmbutton.setOnPic(load_image("prebar_orange.png",-1))
    prebgmbutton.setPos(140,550)
def prebgmbutton_click(sender,event):
    prebgm()

nextbgmbutton=None
def updateNextBgmButton():
    global nextbgmbutton
    nextbgmbutton.setPic(load_image("nextbar.png",-1))
    nextbgmbutton.setOnPic(load_image("nextbar_orange.png",-1))
    nextbgmbutton.setPos(610,550)
def nextbgmbutton_click(sender,event):
    nextbgm()

def showGalleryButtons():
    global buttons
    buttons.empty()
    global menubutton,precgbutton,nextcgbutton,prebgmbutton,nextbgmbutton
    buttons.add(menubutton)
    buttons.add(precgbutton)
    buttons.add(nextcgbutton)
    buttons.add(prebgmbutton)
    buttons.add(nextbgmbutton)

def init_GalleryButtons():
    global menubutton
    menubutton=Button()
    menubutton.run=menubutton_click
    updateMenuButton()
    global precgbutton
    precgbutton=Button()
    precgbutton.run=precgbutton_click
    updatePreCgButton()
    global nextcgbutton
    nextcgbutton=Button()
    nextcgbutton.run=nextcgbutton_click
    updateNextCgButton()
    global prebgmbutton
    prebgmbutton=Button()
    prebgmbutton.run=prebgmbutton_click
    updatePreBgmButton()
    global nextbgmbutton
    nextbgmbutton=Button()
    nextbgmbutton.run=nextbgmbutton_click
    updateNextBgmButton()

cglabel=None
bgmlabel=None
cgcollection=""
nowcg=0
totcg=0
nowbgm=0
totbgm=0
def init_GalleryBasic():
    global story,data,cgcollection
    story=saveload.ldseen()
    data.readdata=saveload.ldread()
    global nowcg,totcg,nowbgm,totbgm
    nowcg=0
    nowbgm=0
    totcg=len(data.readdata.cgs)
    already=0
    for i in data.readdata.cgs:
        if i:
            already+=1
    print already
    cgcollection="CG:%4d%%"%(already*100/(totcg-1))
    totbgm=len(data.readdata.bgms)
    global cglabel,bgmlabel
    cglabel=RichText()
    cglabel.setPic(load_image("textbar.png",-1))
    cglabel.setPos(200,0)
    bgmlabel=RichText()
    bgmlabel.setPic(load_image("textbar.png",-1))
    bgmlabel.setPos(200,550)
    
def init():
    global screen
    screen=pygame.display.get_surface()
    init_GalleryBasic()    
    init_GalleryButtons()

def show():
    global Closed
    Closed=False
    showGalleryButtons()
    setcgindex(0)
    setbgmindex(1)

def remove():
    global Closed
    Closed=True
    global buttons
    buttons.empty()
    global menubutton
    menubutton=None
    global precgbutton
    precgbutton=None
    global nextcgbutton
    nextcgbutton=None
    global prebgmbutton
    prebgmbutton=None
    global nextbgmbutton
    nextbgmbutton=None
    
def eventHandler(event):
    if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_UP:
        precg()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_DOWN:
        nextcg()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_LEFT:
        prebgm()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_RIGHT:
        nextbgm()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_SPACE:
        changeOnlyPic()
        return True
    elif event.type == pygame.locals.MOUSEBUTTONDOWN:
        mouse=pygame.mouse.get_pos()
        for tmpbtn in buttons:
            if tmpbtn.check(mouse):
                tmpbtn.run(tmpbtn,event)
                return True
        else:
            if settings.onlypic:
                changeOnlyPic()
                return True
    elif event.type == pygame.locals.MOUSEMOTION:
        mouse=pygame.mouse.get_pos()
        for tmpbtn in buttons:
            tmpbtn.setMouse(mouse)
    return False

def afterHandle():
    global screen,buttons
    if not settings.onlypic:
        screen.blit(cglabel.image,cglabel.rect)
        screen.blit(bgmlabel.image,bgmlabel.rect)
        buttons.update()
        buttons.draw(screen)
