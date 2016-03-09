# -*- coding: gbk -*-
import pygame
pygame.init()
import threading

from avgbase import *
import lib_avgextend as avgex
import settings
import saveload
import OpenLayer
import MainMenuLayer
import StoryLayer
import GalleryLayer
screen=None
basesprites=None
blackground=None

closing=False

def showSettings():
    pass

def OpenLayer_BackToMenu():
    global layers
    OpenLayer.remove()
    layers.remove(OpenLayer)
    global closing
    if closing:
        close()
    else:
        showMainMenuLayer()

def showOpenLayer():
    global layers
    OpenLayer.init()
    layers.insert(0,OpenLayer)
    OpenLayer.BackToMenu=OpenLayer_BackToMenu
    OpenLayer.show()

def MainMenuLayer_startNewGame():
    global layers
    MainMenuLayer.remove()
    layers.remove(MainMenuLayer)
    showStoryLayer()
    StoryLayer.startNewGame()
    
def MainMenuLayer_loadGame():
    global layers
    MainMenuLayer.remove()
    layers.remove(MainMenuLayer)
    showStoryLayer()
    StoryLayer.loadGame()

def MainMenuLayer_showGallery():
    global layers
    MainMenuLayer.remove()
    layers.remove(MainMenuLayer)
    showGalleryLayer()
    
def MainMenuLayer_close():
    global layers
    MainMenuLayer.remove()
    layers.remove(MainMenuLayer)
    global closing
    closing=True
    showOpenLayer()
    
def showMainMenuLayer():
    global layers
    MainMenuLayer.init()
    layers.insert(0,MainMenuLayer)
    MainMenuLayer.show()
    MainMenuLayer.startNewGame=MainMenuLayer_startNewGame
    MainMenuLayer.loadGame=MainMenuLayer_loadGame
    MainMenuLayer.showGallery=MainMenuLayer_showGallery
    MainMenuLayer.close=MainMenuLayer_close

def StoryLayer_BackToMenu():
    global layers
    StoryLayer.remove()
    layers.remove(StoryLayer)
    showMainMenuLayer()
    
def showStoryLayer():
    global layers
    StoryLayer.init()
    layers.insert(0,StoryLayer)
    StoryLayer.show()
    StoryLayer.BackToMenu=StoryLayer_BackToMenu

def GalleryLayer_BackToMenu():
    global layers
    GalleryLayer.remove()
    layers.remove(GalleryLayer)
    showMainMenuLayer()
    
def showGalleryLayer():
    global layers
    GalleryLayer.init()
    layers.insert(0,GalleryLayer)
    GalleryLayer.show()
    GalleryLayer.BackToMenu=GalleryLayer_BackToMenu
    
def close():
    pygame.display.quit()
    pygame.mixer.music.stop()
    return 0
    
layers=[]
def mainloop():
    global screen,blackground,basesprites
    global layers
    clock = pygame.time.Clock()
    showOpenLayer()
    try:
        while True:
            clock.tick(30)
            screen.blit(blackground,(0,0))
            basesprites.update()
            basesprites.draw(screen)
            for layer in layers:
                layer.preHandle()
            for event in pygame.event.get():
                if event.type==pygame.locals.MOUSEBUTTONDOWN and settings.wait:
                    continue
                handled=False
                if event.type == pygame.locals.QUIT:
                    handled=True
                    return close()
                elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                    handled=True
                    return close()
                elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_RETURN and event.mod & pygame.locals.KMOD_ALT:
                    settings.fullscreen=not settings.fullscreen
                    if settings.fullscreen:
                        screen = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600))
                else:
                    for layer in layers:
                        handled=layer.eventHandler(event)
                        if handled:
                            break
                if not handled:
                    pass
            for layer in layers:
                layer.afterHandle()
                if layer.Closed:
                    try:
                        layers.remove(layer)
                    except:
                        pass
            empty=True
            for layer in layers:
                if not layer.Closed:
                    empty=False
            if empty:
                return close()
            pygame.display.flip()
    finally:
        pygame.display.quit()

def init():
    global screen,blackground,basesprites
    screen = pygame.display.set_mode((800, 600))
    from lib_img import load_image
    icon,rect=load_image("icon.png",-1)
    pygame.display.set_icon(icon)
    if settings.fullscreen:
        screen = pygame.display.set_mode((800, 600),pygame.FULLSCREEN)
    pygame.display.set_caption('Sinners')
    blackground = screen.convert()
    blackground.fill((0, 0, 0))
    screen.blit(blackground,(0,0))
    avgex.init()
    basesprites=avgex.getRender()
    
if __name__=="__main__":
    #try:
    init()
    mainloop()
    """
    except Exception ,message:
        print message
    finally:
        raw_input()
        """
        
