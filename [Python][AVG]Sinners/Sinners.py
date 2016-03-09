#coding:gbk
import os,sys
os.environ['SDL_VIDEODRIVER'] = 'windib'
def chkpyg():
    try:
        import pygame
        print "Import pygame success"
        return True
    except :
        try:
            if sys.version[:3]=="2.6":
                print "python version:2.6"
                sys.path.append(os.path.join(os.path.abspath("."),"Lib26"))
                import pygame
                return True
            elif sys.version[:3]=="2.7":
                print "python version:2.7"
                sys.path.append(os.path.join(os.path.abspath("."),"Lib27"))
                import pygame
                return True
            else:
                raise
        except:
            print "请下载安装对应版本pygame"
            print "www.pygame.org/download"
            return False
sys.path.insert(0,os.path.join(os.path.abspath("."),"src"))
import settings
settings.setAppPath(".")

import front
class App:
    def run(self):
        front.init()
        front.mainloop()
        return 0
    
import threading,Queue
queue=Queue.Queue()
class EmptyThread(threading.Thread):
    stop=False
    def run(self):
        global queue
        queue.get()
            
if __name__=="__main__":
    th=EmptyThread()
    th.start()
    if chkpyg():
        app=App()
        if app.run()==0:
            queue.put("stop")
