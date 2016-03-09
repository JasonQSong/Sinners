import pygame
pygame.init()
if not pygame.mixer:
    raise "pygame.mixer is disabled"
import settings

def load_music(name):
    import os
    fullname = os.path.join(settings.bgmpath, name)
    try:
        pygame.mixer.music.load(fullname)
    except pygame.error, message:
        print 'Cannot load music:', fullname
        raise SystemExit, message
    return pygame.mixer.music

def load_bgm(name,start=0.0):
    class BgmMusic:
        def play(self):
            load_music(name)
            pygame.mixer.music.play(-1)
    return BgmMusic()

def test():
    load_bgm("love song.mp3").play()

if __name__=="__main__":
    test()
