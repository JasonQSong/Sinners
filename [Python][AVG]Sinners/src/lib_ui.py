import pygame
pygame.init()
from lib_font import Font
from lib_img import load_image
import lib_avgextend as avgex

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.clear()
    def clear(self):
        self.image=None
        self.rect=None
    def setPic(self,(image,rect)):
        self.image=image
        self.rect=rect
    def setPos(self,x,y):
        self.rect.x=x
        self.rect.y=y

class RichText(Sprite):
    def __init__(self,fontfile=None,fontsize=30,txt="",txtpos=(0,0),color=(255,255,255)):
        Sprite.__init__(self)
        if fontfile==None:
            self.font=Font(fontsize)
        else:
            self.font=Font(fontsize,fontfile)
        self.txt=txt
        self.txtpos=txtpos
        self.color=color
    def setColor(r,g,b):
        self.color=(r,g,b)
        self.setTxt(self.txt,self.txtpos)
    def setPic(self,(image,rect)):
        self.background=image.copy()
        self.image=image
        self.rect=rect
    def setTxt(self,txt,(x,y)):
        self.txt=txt
        self.txtpos=(x,y)
        self.image=self.background.copy()
        self.image.blit(self.font.render(txt,1,self.color),pygame.Rect(x,y,0,0))
        
class Button(RichText):
    offbackground=None
    offimage=None
    onbackground=None
    onimage=None
    focus=False
    def setFocus(self,val):
        self.focus=val
        if val:
            avgex.playwav("s00.wav")
            self.image=self.onimage
        else:
            self.image=self.offimage
            
    def setPic(self,(image,rect)):
        RichText.setPic(self,(image,rect))
        self.offbackground=image.copy()
        self.offimage=image
        self.onbackground=image.copy()
        self.onimage=image
    def setOnPic(self,(image,rect)):
        self.onbackground=image.copy()
        self.onimage=image
    def setTxt(self,txt,(x,y)):
        RichText.setTxt(self,txt,(x,y))
        self.onimage=self.onbackground.copy()
        self.onimage.blit(self.font.render(txt,1,self.color),pygame.Rect(x,y,0,0))
        self.offimage=self.offbackground.copy()
        self.offimage.blit(self.font.render(txt,1,self.color),pygame.Rect(x,y,0,0))
    def setOnTxt(self,txt,(x,y)):
        self.onimage=self.onbackground.copy()
        self.onimage.blit(self.font.render(txt,1,self.color),pygame.Rect(x,y,0,0))
        
    def run(self,sender,event):
        pass
    def check(self,(x,y)):
        if self.rect.colliderect(pygame.Rect(x,y,1,1)):
            return True
        return False
    def setMouse(self,(x,y)):
        if self.focus!=self.check((x,y)):
            self.focus=not self.focus
            if self.focus:
                self.setFocus(True)
            else:
                self.setFocus(False)
        return self.focus

class BackGroundSprite(Sprite):
    def clear(self):
        self.setPic(load_image("black.jpg"))

class ForeGroundSprite(Sprite):
    def clear(self):
        self.setPic(load_image(""))
