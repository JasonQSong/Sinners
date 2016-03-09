import pygame
pygame.init()
if not pygame.font:
    raise "pygame.font is disabled"
pygame.font.init()
import settings

def Font(size=30,filename=None):
    if filename==None:
        filename=settings.font
    import os
    fullname=os.path.join(settings.fontpath,filename)
    font=pygame.font.Font(fullname,size)
    return font

def test():
    Font("simhei.ttf",30)

if __name__=="__main__":
    test()
