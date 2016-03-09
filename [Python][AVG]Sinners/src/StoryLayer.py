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

import Queue
queue=Queue.Queue()

class Game_Data:
    readdata=None
    gamedata=None
data=Game_Data()

class SelectBtn(Button):
    tar=0
    index=0
    def __init__(self):
        Button.__init__(self)
        self.setPic(load_image("selection.png",-1))
        self.setOnPic(load_image("selection_orange.png",-1))
    def setTxt(self,txt):
        Button.setTxt(self,txt,(80,15))

class StoryThread(threading.Thread):
    data=None
    settings=None
    queue=None
    condition=threading.Condition()
    disposed=False
    def pause(self):
        self.settings.pause=True
        if threading.currentThread().getName()!="storyThread":
            return None
        self.condition.acquire()
        self.condition.wait()
        self.condition.release()
    def conti(self):
        if not self.settings.pause:
            return None
        if settings.waitforchoose:
            return None
        self.settings.pause=False
        self.condition.acquire()
        self.condition.notifyAll()
        self.condition.release()
    def __init__(self,data,settings,queue):
        threading.Thread.__init__(self,name="storyThread")
        self.data=data
        self.settings=settings
        self.queue=queue
        self.daemon=True
    def run(self):
        d=self.data
        global story
        doc=story.doc
        settings=self.settings
        settings.pause=False
        q=self.queue
        XEplots=story.XEplots
        clock=pygame.time.Clock()
        self.pause()
        while True:
            clock.tick(60)
            if self.disposed:
                return None
            if settings.pause:
                self.pause()
            if settings.wait:
                continue
            if d.gamedata.pl==0:
                q.put(("exit",))
                break
            pl=XEplots.childNodes[d.gamedata.pl]
            st=pl.childNodes[0].childNodes[d.gamedata.st]
            view=Me(doc,st)
            if view.rt.tagName=="sentence":
                peo=view.gtat("peo")
                txt=view.gtat("txt")
                voc=eval(view.gtat("voc"))
                tmp=""
                q.put(("voc",voc))
                d.gamedata.peo=peo
                d.gamedata.txt=txt
                if not settings.skipping:
                    for i in txt:
                        tmp+=i
                        q.put(("se",peo,tmp))
                        if settings.pause:
                            break
                        pygame.time.delay(settings.delay_char)
                q.put(("se",peo,txt))
                pygame.time.delay(settings.delay_sentence)
                if (not settings.auto) and (not settings.skipping):
                    self.pause()
            elif view.rt.tagName=="cg":
                tar=eval(view.gtat("tar"))
                q.put(("cg",tar))
                d.readdata.cgs[tar]=True
                settings.wait=True
            elif view.rt.tagName=="bgm":
                tar=eval(view.gtat("tar"))
                q.put(("bgm",tar))
            elif view.rt.tagName=="wav":
                name=view.gtat("name")
                q.put(("wav",name))
            elif view.rt.tagName=="bg":
                tar=eval(view.gtat("tar"))
                way=view.gtat("way")
                q.put(("bg",tar,way))
                settings.wait=True
            elif view.rt.tagName=="fg":
                tar=eval(view.gtat("tar"))
                spr=eval(view.gtat("spr"))
                fin=eval(view.gtat("fin"))
                beg=eval(view.gtat("beg"))
                way=view.gtat("way")
                q.put(("fg",tar,spr,fin,beg,way))
            elif view.rt.tagName=="ch":
                tar=eval(view.gtat("tar"))
                XEchos=view.rt.getElementsByTagName("choise")
                chos=[]
                for i in range(len(XEchos)):
                    txt=XEchos[i].getAttribute("txt")
                    factor=XEchos[i].getAttribute("factor")
                    chos+=[(txt,factor)]
                q.put(("ch",tar,chos))
                settings.waitforchoose=True
                self.pause()
            elif view.rt.tagName=="jp":
                tar=eval(view.gtat("tar"))
                factor=view.gtat("factor")
                s=d.gamedata.selects
                if(eval(factor)):
                    d.gamedata.pl=tar
                    d.gamedata.st=0
            else:
                pass
            d.readdata.plots[d.gamedata.pl][0]=True
            d.readdata.plots[d.gamedata.pl][d.gamedata.st]=True
            print "pl:%d st:%d"%(d.gamedata.pl,d.gamedata.st)
            d.gamedata.st+=1
            if d.gamedata.st>=len(pl.childNodes[0].childNodes):
                d.gamedata.pl=0
        return None
storyThread=None

def changeOnlyPic():
    global settings
    global storyThread
    if settings.onlypic:
        settings.onlypic=False
    else:
        storyThread.pause()
        settings.onlypic=True

def startNewGame():
    global data,storyThread
    data.gamedata.pl=1
    data.gamedata.st=1
    showStoryButtons()
    storyThread.conti()
    
def showChoises(tar,chos):
    global buttons,data,storyThread
    for i in range(1,len(chos)):
        tmpbtn=SelectBtn()
        tmpbtn.setPos(100,100+80*i)
        tmpbtn.setTxt(chos[i][0])
        tmpbtn.tar=tar
        tmpbtn.index=i
        tmpbtn.run=choisebutton_click
        buttons.add(tmpbtn)

def choisebutton_click(sender,event):
    global buttons,data,storyThread
    data.gamedata.selects[sender.tar]=sender.index
    settings.waitforchoose=False
    showStoryButtons()
    storyThread.conti()

def setSkip(val):
    global settings,storyThread
    if val:
        settings.skipping=True
        settings.delay_char=0
        settings.delay_sentence=100
        storyThread.conti()
        return None
    settings.skipping=False
    settings.delay_char=70
    settings.delay_sentence=300
    
def setAuto(value):
    global settings,storyThread
    settings.auto=value
    updateAutoButton()
    if settings.auto:
        storyThread.conti()
def changeAuto():
    global settings
    setAuto(not settings.auto)

def loadGame():
    global font,peoplerender,people,textrender,text
    data.gamedata=saveload.ldgame(1)
    avgex.setbg(data.gamedata.bg)
    avgex.playbgm(data.gamedata.bgm)
    people=data.gamedata.peo
    text=data.gamedata.txt
    peoplerender=font.render(people,1,(255,255,255))
    textrender=[]
    for i in range(5):
        tmp=text[20*i:20*(i+1)]
        if tmp=="":
            break
        textrender+=[font.render(tmp,1,(255,255,255))]

menubutton=None
def updateMenuButton():
    global settings,memubutton
    menubutton.setPic(load_image("littlebutton_orange.png",-1))
    menubutton.setOnTxt("Menu",(10,5))
    menubutton.setPos(360,560)
def menubutton_click(sender,event):
    settings.waitforchoose=False
    BackToMenu()
    
autobutton=None
def updateAutoButton():
    global settings,autobutton
    if settings.auto:
        autobutton.setPic(load_image("littlebutton_yello.png",-1))
    else:
        autobutton.setPic(load_image("littlebutton.png",-1))
    autobutton.setOnTxt("Auto",(10,5))
    autobutton.setPos(10,560)
def autobutton_click(sender,event):
    changeAuto()

historybutton=None
def updateHistoryButton():
    pass
def historybutton_click(sender,event):
    pass

nextbutton=None
def updateNextButton():
    pass
def nextbutton_click(sender,event):
    pass

loadbutton=None
def updateLoadButton():
    global settings,loadbutton
    loadbutton.setPic(load_image("littlebutton.png",-1))
    loadbutton.setOnTxt("Load",(10,5))
    loadbutton.setPos(630,560)
def loadbutton_click(sender,event):
    global storyThread
    storyThread.pause()
    waitforchoose=False
    showStoryButtons()
    loadGame()
        
savebutton=None
def updateSaveButton():
    global settings,savebutton
    savebutton.setPic(load_image("littlebutton.png",-1))
    savebutton.setOnTxt("Save",(10,5))
    savebutton.setPos(710,560)
def savebutton_click(sender,event):
    global storyThread,data
    storyThread.pause()
    data.gamedata.st-=1
    saveload.svgame(data.gamedata,1)
    data.gamedata.st+=1
    saveload.svread(data.readdata)

settingsbutton=None
def updateSettingsButton():
    pass
def settingsbutton_click(sender,event):
    pass

def showStoryButtons():
    global buttons
    buttons.empty()
    global menubutton,autobutton,loadbutton,savebutton
    buttons.add(menubutton)
    buttons.add(autobutton)
    buttons.add(loadbutton)
    buttons.add(savebutton)

def init_StoryButtons():
    global menubutton
    menubutton=Button()
    menubutton.run=menubutton_click
    updateMenuButton()
    global autobutton
    autobutton=Button()
    autobutton.run=autobutton_click
    updateAutoButton()
    global historybutton
    historybutton=Button()
    historybutton.run=historybutton_click
    global nextbutton
    nextbutton=Button()
    nextbutton.run=nextbutton_click
    global loadbutton
    loadbutton=Button()
    loadbutton.run=loadbutton_click
    updateLoadButton()
    global savebutton
    savebutton=Button()
    savebutton.run=savebutton_click
    updateSaveButton()
    global settingsbutton
    settingsbutton=Button()
    settingsbutton.run=settingsbutton_click

font=None
peopleboarder=None
textboarder=None
peoplerender=None
people=""
textrender=[]
text=""
def init_StoryBasic():
    global story,data,storyThread,queue
    story=saveload.ldseen()
    data.readdata=saveload.ldread()
    data.gamedata=saveload.ldgame(0)
    storyThread=StoryThread(data,settings,queue)
    storyThread.start()
    global font,peopleboarder,peoplerender,people,textboarder,textrender,text
    font = Font()
    peopleboarder=Sprite()
    peopleboarder.setPic(load_image("peoboard.png",-1))
    peopleboarder.setPos(0,350)
    peoplerender=font.render("",1,(255,255,255))
    people=""
    textboarder=Sprite()
    textboarder.setPic(load_image("txtboard.png",-1))
    textboarder.setPos(0,400)
    textrender=[]
    text=""
    
def init():
    global screen
    screen=pygame.display.get_surface()
    init_StoryBasic()    
    init_StoryButtons()

def show():
    global Closed
    Closed=False
    showStoryButtons()

def remove():
    global data
    saveload.svread(data.readdata)
    global storyThread
    storyThread.disposed=True
    storyThread=None
    global Closed
    Closed=True
    global buttons
    buttons.empty()
    global menubutton
    menubutton=None
    global autobutton
    autobutton=None
    global historybutton
    historybutton=None
    global nextbutton
    nextbutton=None
    global loadbutton
    loadbutton=None
    global savebutton
    savebutton=None
    global settingsbutton
    settingsbutton=None
    
def eventHandler(event):
    if event.type == pygame.locals.KEYDOWN and (event.key == pygame.locals.K_LCTRL or event.key == pygame.locals.K_RCTRL):
        setSkip(True)
        return True
    elif event.type == pygame.locals.KEYUP and (event.key == pygame.locals.K_LCTRL or event.key == pygame.locals.K_RCTRL):
        setSkip(False)
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_SPACE:
        changeOnlyPic()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_s:
        startNewGame()
        return True
    elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_c:
        storyThread.conti()
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
            else:
                storyThread.conti()
                return True
    elif event.type == pygame.locals.MOUSEMOTION:
        mouse=pygame.mouse.get_pos()
        for tmpbtn in buttons:
            tmpbtn.setMouse(mouse)
    return False

def afterHandle():
    global story,data
    global peopleboarder,textboarder,font,peoplerender,people,textrender,text
    while True:
        try:
            para=queue.get_nowait()
            tp=para[0]
            if tp!="se":
                print para
            if tp=="exit":
                BackToMenu()
                return
            if tp=="se" :
                peo=para[1]
                txt=para[2]
                peoplerender=font.render(peo,1,(255,255,255))
                people=peo
                textrender=[]
                text=txt
                for i in range(5):
                    tmp=txt[20*i:20*(i+1)]
                    if tmp=="":
                        break
                    textrender+=[font.render(tmp,1,(255,255,255))]
            elif tp=="cg":
                tar=para[1]
                XEcg=story.XEcgs.getElementsByTagName("cg")[tar]
                filename=XEcg.getAttribute("name")
                data.gamedata.bg=filename
                avgex.setcg(filename)
            elif tp=="bgm":
                tar=para[1]
                XEbgm=story.XEbgms.getElementsByTagName("bgm")[tar]
                filename=XEbgm.getAttribute("name")
                data.gamedata.bgm=filename
                avgex.playbgm(filename)
            elif tp=="wav":
                name=para[1]
                avgex.playwav(name)
            elif tp=="bg":
                tar=para[1]
                way=para[2]
                XEbg=story.XEbgs.getElementsByTagName("bg")[tar]
                filename=XEbg.getAttribute("name")
                data.gamedata.bg=filename
                avgex.setbg(XEbg.getAttribute("name"))
            elif tp=="bgalpha":
                alpha=para[1]
                avgex.setbgalpha(alpha)
            elif tp=="bgend":
                tar=para[1]
                way=para[2]
                XEbg=story.XEbgs.getElementsByTagName("bg")[tar]
                filename=XEbg.getAttribute("name")
                data.gamedata.bg=filename
                avgex.setbottom(XEbg.getAttribute("name"))
            elif tp=="fg":
                tar=para[1]
                spr=para[2]
                fin=para[3]
                beg=para[4]
                way=para[5]
                XEfg=story.XEfgs.getElementsByTagName("fg")[tar]
                avgex.setfg(XEfg.getAttribute("name"),spr,fin)
            elif tp=="ch":
                tar=para[1]
                chos=para[2]
                showChoises(tar,chos)
            else:
                pass
        except Queue.Empty:
            break
    if not settings.onlypic:
        if people!="":
            screen.blit(peopleboarder.image,peopleboarder.rect)
            screen.blit(peoplerender,pygame.Rect(50,360,0,0))
        if text!="":
            screen.blit(textboarder.image,textboarder.rect)
            for i in range(len(textrender)):
                screen.blit(textrender[i],pygame.Rect(50,420+40*i,0,0))
        global buttons
        buttons.update()
        buttons.draw(screen)
