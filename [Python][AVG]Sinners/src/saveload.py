# -*- coding: cp936 -*-
import cPickle as _p
from avgbase import *
import os
import settings

def svseen(story,ver=""):
    global seenpath
    fullname=os.path.join(settings.seenpath,"seen.xml")
    if ver!="":
        fullname=os.path.join(settings.seenpath,"seen_ver%s.xml"%ver)
    f=open(fullname,'w')
    story.doc.writexml(f,addindent="",newl="",encoding="utf-8")
    f.close()

def ldseen(ver=""):
    global seenpath
    fullname=os.path.join(settings.seenpath,"seen.xml")
    if ver!="":
        fullname=os.path.join(settings.seenpath,"seen_ver%s.xml"%ver)
    doc=minidom.parse(fullname)
    rt=doc.documentElement
    story=Story(doc,rt)
    return story

def svgame(game,i):
    fullname=os.path.join(settings.savepath,"SAV%d.sav"%i)
    f=file(fullname,'w')
    _p.dump(game,f)
    f.close()
    
def ldgame(i):
    if(i==0):
        return newgame()
    fullname=os.path.join(settings.savepath,"SAV%d.sav"%i)
    if os.path.exists(fullname):
        f=file(fullname)
        game=_p.load(f)
    else:
        raise "No Game Data: %d"%i
    return game

def newgame():
    return GameData(ldseen())

def svread(read):
    fullname=os.path.join(settings.savepath,"read.sav")
    f=file(fullname,'w')
    _p.dump(read,f)
    f.close()

def ldread():
    fullname=os.path.join(settings.savepath,"read.sav")
    if os.path.exists(fullname):
        f=file(fullname)
        read=_p.load(f)
    else:
        story=ldseen()
        read=ReadData(story)
        svread(read)
    return read

if __name__=="__main__":
    pass
