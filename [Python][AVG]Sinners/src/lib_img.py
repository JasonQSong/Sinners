import pygame
pygame.init()
import settings

def load_image(name, colorkey=None):
    import os
    
    if name=="":
        name="trans.png"
        colorkey=-1
        
    fullname = os.path.join(settings.imgpath, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if colorkey is not None:
        if colorkey is -1:
            image.convert_alpha()
        else:
            image=image.convert()
            if colorkey == -2:
                colorkey=image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
    else:
        image = image.convert()
    return image, image.get_rect()

def test():
    load_image("title.jpg")

if __name__=="__main__":
    test()
