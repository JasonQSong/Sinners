# -*- coding: utf-8 -*-
import os, sys
import pygame
pygame.init()
import pygame.locals
#from pygame.locals import *
import settings
import lib_font
from lib_font import Font
import lib_img
from lib_img import load_image
import lib_bgm
from lib_bgm import load_bgm
import lib_wav
from lib_wav import load_wav

from lib_ui import *
import settings

screen=None
bottomsprite=None
backgroundsprite=None
foregroundsprites=[None for i in range(6)]
blackground=None
whiteground=None
def clearfg():
    global foregroundsprites
    for i in foregroundsprites:
        i.clear()
def setcg(name):
    clearfg()
    setbg(name)
import threading
class fadeOutThread(threading.Thread):
    name=""
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name
        self.daemon=True
    def run(self):
        if True:
            fadeoutms=settings.fadeoutms/25
            for i in range(0,256,10):
                setbgalpha(i)
                pygame.time.delay(fadeoutms)
            setbottom(self.name)
            settings.wait=False
        
def setbottom(name):
    global bottomsprite
    bottomsprite.setPic(load_image(name))
def setbgalpha(i):
    global backgroundsprite
    backgroundsprite.image.set_alpha(i)
def setbg(name):
    if name=="":
        raise
    global bottomsprite,backgroundsprite
    backgroundsprite.image.set_alpha(0)
    backgroundsprite.setPic(load_image(name))
    settings.wait=True
    fadeOutThread(name).start()
    
def setfg(name,i,fin):
    global foregroundsprites
    if name=="":
        foregroundsprites[i].clear()
        return None
    image,rect=load_image(name,-1)
    foregroundsprites[i].setPic((image,rect))
    foregroundsprites[i].setPos(fin-(rect.w)/2,0)

def playwav(name):
    if name=="":
        return False
    load_wav(name).play()

def playbgm(name,start=0.0):
    if name=="":
        return False
    load_bgm(name,start).play()

def getRender():
    global backgroundsprite,foregroundsprites
    group=pygame.sprite.OrderedUpdates((bottomsprite,\
                                        backgroundsprite,\
                                        foregroundsprites[1],\
                                        foregroundsprites[2],\
                                        foregroundsprites[3],\
                                        foregroundsprites[4],\
                                        foregroundsprites[5]\
                                        ))
    return group

def init():
    global screen
    global bottomsprite,backgroundsprite,foregroundsprites
    global blackground,whiteground
    screen=pygame.display.get_surface()
    bottomsprite=BackGroundSprite()
    bottomsprite.image=screen.convert()
    bottomsprite.image.fill((0,0,0))
    backgroundsprite=BackGroundSprite()
    backgroundsprite.setPic(load_image("title.jpg"))
    for i in range(6):
        foregroundsprites[i]=ForeGroundSprite()
        foregroundsprites[i].setPic(load_image("",-1))
    blackground = screen.convert()
    blackground.fill((0, 0, 0))
    whiteground = screen.convert()
    whiteground.fill((255, 255, 255))
"""
class Fist(pygame.sprite.Sprite):
    "moves a clenched fist on the screen, following the mouse"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fg1.png', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0

class Chimp(pygame.sprite.Sprite):
    ""moves a monkey critter across the screen. it can spin the
       monkey when it is punched.""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('fg1.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
"""
def test():
    global backgroundsprite,screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    playbgm("02 hope.mp3")

    if pygame.font:
        font = pygame.font.Font(None, 10)
        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)


    screen.blit(background, (0, 0))
    pygame.display.flip()


    whiff_sound = load_wav('ame.wav')
    punch_sound = load_wav('don.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((chimp,fist))
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.display.quit()
            elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
                    playbgm("03 love song.mp3")
                    showcg("bg1.jpg")
            elif event.type == pygame.locals.MOUSEBUTTONUP:
                fist.unpunch()
                
        allsprites.update()
        
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()


if __name__=="__main__":
    pygame.init()
    init()
