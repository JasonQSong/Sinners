import pygame
pygame.init()
if not pygame.mixer:
    raise "pygame.mixer is disabled"
import settings
    
def load_sound(name):
    import os
    fullname = os.path.join(settings.wavpath, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def load_wav(name):
    return load_sound(name)

def test():
    load_wav("bung.wav").play()

if __name__=="__main__":
    test()
