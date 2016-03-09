# class Story
from xml.dom import minidom
class GameData:
    selects=[0]
    pl=0
    st=0
    bg=""
    bgm=""
    peo=""
    txt=""
    def __init__(self,story):
        self.getrangeByStory(story)
        
    def getrangeByStory(self,story):
        rt=story.rt
        self.selects=[0 for i in range(eval(rt.getAttribute("selects"))+1)]

class ReadData:
    plots=[[]]
    cgs=[False]
    bgms=[False]
    bgs=[False]
    fgs=[False]
    def __init__(self,story):
        self.getrangeByStory(story)
        
    def getrangeByStory(self,story):
        rt=story.rt
        self.plots=[[]]
        XEcgs=rt.getElementsByTagName("cgs")[0]
        XEbgms=rt.getElementsByTagName("bgms")[0]
        XEbgs=rt.getElementsByTagName("bgs")[0]
        XEfgs=rt.getElementsByTagName("fgs")[0]
        XEplots=rt.getElementsByTagName("plots")[0]
        self.cgs=[False for i in range(len(XEcgs.childNodes))]
        self.bgms=[False for i in range(len(XEbgms.childNodes))]
        self.bgs=[False for i in range(len(XEbgs.childNodes))]
        self.fgs=[False for i in range(len(XEfgs.childNodes))]
        for i in range(1,len(XEplots.childNodes)):
            XEplot=XEplots.childNodes[i]
            XEsteps=XEplot.childNodes[0]
            tmp=[False for j in range(len(XEsteps.childNodes))]
            self.plots+=[tmp]

class Me(object):
    """Member"""
    tp="Me"
    doc=None
    rt=None
    exist=True
    def __init__(self,doc,rt):
        self.tp="Me"
        self.doc=doc
        self.rt=rt

    def __str__(self):
        if rt==None:
            return object.__str__(self) 
        return self.rt.toxml(encoding="utf-8")

    def gtat(self,attr):
        """get root attribute"""
        if (self.rt.hasAttribute(attr)):
            return self.rt.getAttribute(attr)
        raise "%s don't have the attribute: %s"%(self.tp,attr)

    def stat(self,attr,val):
        """set root attribute"""
        self.rt.attributes[attr]=val
        
class Story(Me):
    XEcgs=None
    XEbgms=None
    XEbgs=None
    XEfgs=None
    XEplots=None
    def __init__(self,doc,rt):
        self.tp="Story"
        Me.__init__(self,doc,rt)
        self.build()
        
    def build(self):
        if(self.rt.hasAttribute("selects")):
            self.XEcgs=self.rt.getElementsByTagName("cgs")[0]
            self.XEbgms=self.rt.getElementsByTagName("bgms")[0]
            self.XEbgs=self.rt.getElementsByTagName("bgs")[0]
            self.XEfgs=self.rt.getElementsByTagName("fgs")[0]
            self.XEplots=self.rt.getElementsByTagName("plots")[0]
        else:
            self.rt.attributes["selects"]="%d"%0
            
            self.XEcgs=self.doc.createElement("cgs")
            self.rt.appendChild(self.XEcgs)
            self.addcg("")
            
            self.XEbgms=self.doc.createElement("bgms")
            self.rt.appendChild(self.XEbgms)
            self.addbgm("")
            
            self.XEbgs=self.doc.createElement("bgs")
            self.rt.appendChild(self.XEbgs)
            self.addbg("")
            
            self.XEfgs=self.doc.createElement("fgs")
            self.rt.appendChild(self.XEfgs)
            self.addfg("")
            
            self.XEplots=self.doc.createElement("plots")
            self.rt.appendChild(self.XEplots)
            self.addPl()

            self.init()

    def init(self):
        pass

    def setselects(self,num):
        self.rt.attributes["selects"]="%d"%num

    def addcg(self,name):
        XEcg=self.doc.createElement("cg")
        XEcg.attributes["id"]="%d"%(len(self.XEcgs.childNodes))
        XEcg.attributes["name"]=name
        self.XEcgs.appendChild(XEcg)
        return XEcg
        
    def addbgm(self,name):
        XEbgm=self.doc.createElement("bgm")
        XEbgm.attributes["id"]="%d"%(len(self.XEbgms.childNodes))
        XEbgm.attributes["name"]=name
        self.XEbgms.appendChild(XEbgm)
        return XEbgm
        
    def addbg(self,name):
        XEbg=self.doc.createElement("bg")
        XEbg.attributes["id"]="%d"%(len(self.XEbgs.childNodes))
        XEbg.attributes["name"]=name
        self.XEbgs.appendChild(XEbg)
        return XEbg
        
    def addfg(self,name):
        XEfg=self.doc.createElement("fg")
        XEfg.attributes["id"]="%d"%(len(self.XEfgs.childNodes))
        XEfg.attributes["name"]=name
        self.XEfgs.appendChild(XEfg)
        return XEfg
    
    def addPl(self):
        XEpl=self.doc.createElement("plot")
        XEpl.attributes["id"]="%d"%(len(self.XEplots.childNodes))
        self.XEplots.appendChild(XEpl)
        pl=Pl(self.doc,XEpl)
        pl.build()
        return XEpl

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")
    
class Pl(Me):
    """Plot"""
    XEsteps=None
    def __init__(self,doc,rt):
        self.tp="Pl"
        Me.__init__(self,doc,rt)
        self.build()

    def build(self):        
        if(len(self.rt.getElementsByTagName("steps"))>0):
            self.XEsteps=self.rt.getElementsByTagName("steps")[0]
        else:
            self.XEsteps=self.doc.createElement("steps")
            self.rt.appendChild(self.XEsteps)
            self.addSe()
            
            self.init()

    def init(self):
        pass

    def addSe(self):
        XEse=self.doc.createElement("sentence")
        XEse.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEse)
        se=Se(self.doc,XEse)
        return XEse

    def addCg(self):
        XEcg=self.doc.createElement("cg")
        XEcg.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEcg)
        cg=Cg(self.doc,XEcg)
        return XEcg
    
    def addBgm(self):
        XEbgm=self.doc.createElement("bgm")
        XEbgm.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEbgm)
        bgm=Bgm(self.doc,XEbgm)
        return XEbgm
    
    def addWav(self):
        XEwav=self.doc.createElement("wav")
        XEwav.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEwav)
        wav=Wav(self.doc,XEwav)
        return XEwav

    def addBg(self):
        XEbg=self.doc.createElement("bg")
        XEbg.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEbg)
        bg=Bg(self.doc,XEbg)
        return XEbg
    
    def addFg(self):
        XEfg=self.doc.createElement("fg")
        XEfg.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEfg)
        fg=Fg(self.doc,XEfg)
        return XEfg
        
    def addCh(self):
        XEch=self.doc.createElement("ch")
        XEch.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEch)
        ch=Ch(self.doc,XEch)
        return XEch
            
    def addJp(self):
        XEjp=self.doc.createElement("jp")
        XEjp.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEjp)
        jp=Jp(self.doc,XEjp)
        return XEjp

    def addSp(self):
        XEsp=self.doc.createElement("sp")
        XEsp.attributes["id"]="%d"%(len(self.XEsteps.childNodes))
        self.XEsteps.appendChild(XEsp)
        sp=Sp(self.doc,XEsp)
        return XEsp
    
    def __str__(self):
        buff="Pl(Plot): Steps=%d"%(len(self.steps)-1)
        for i in range(1,len(self.steps)):
            if not self.steps[i].exist:
                continue
            buff+="\nStep%d:"%i + str(self.steps[i])
        return buff

class St(Me):
    """Step"""
    def __init__(self,doc,rt):
        self.tp="St"
        Me.__init__(self,doc,rt)
    
class Se(St):
    """Sentence"""
    def __init__(self,doc,rt):
        self.tp="Se"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("peo")):
            pass
        else:
            self.init()
        
    def init(self,peo="people",txt="text",voc=0):
        self.rt.attributes["peo"]=peo
        self.rt.attributes["txt"]=txt
        self.rt.attributes["voc"]="%d"%voc
        
    def __str__(self):
        return "Se(Sentence): W=%s"%self.who + ", T=%s"%self.text + ", V=%d"%self.voice

class Cg(St):
    """Computer Graphics"""
    def __init__(self,doc,rt):
        self.tp="Cg"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            pass
        else:
            self.init()
        
    def init(self,tar=0):
        self.rt.attributes["tar"]="%d"%(tar)

class Bgm(St):
    """Back Ground Music"""
    def __init__(self,doc,rt):
        self.tp="Bgm"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            pass
        else:
            self.init()
        
    def init(self,tar=0):
        self.rt.attributes["tar"]="%d"%(tar)
        
class Wav(St):
    """Back Ground Music"""
    def __init__(self,doc,rt):
        self.tp="Wav"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("name")):
            pass
        else:
            self.init()
        
    def init(self,name=""):
        self.rt.attributes["name"]=name

class Bg(St):
    """Back Ground Picture"""
    def __init__(self,doc,rt):
        self.tp="Bg"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            pass
        else:
            self.init()
        
    def init(self,tar=0,way=""):
        "tar:the target picture\n" + \
        "way:the way of the sprite appear(default is fade in)\n" + \
        "   way in ['','flash']"
        self.rt.attributes["tar"]="%d"%(tar)
        self.rt.attributes["way"]=way

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")

class Fg(St):
    """Fore Ground Picture"""
    def __init__(self,doc,rt):
        self.tp="Fg"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            pass
        else:
            self.init()
            
    def init(self,tar=0,spr=0,fin=400,beg=400,way=""):
        "tar:the target picture\n" + \
        "spr:the sprite of the screen\n" + \
        "fin:the final X of the sprite\n" + \
        "beg:the begining X of the sprite (all in 1 second)\n" + \
        "way:the way of the sprite appear(default is fade in)\n" + \
        "   way in ['','flash']"
        self.rt.attributes["tar"]="%d"%(tar)
        self.rt.attributes["spr"]="%d"%(spr)
        self.rt.attributes["fin"]="%d"%(fin)
        self.rt.attributes["beg"]="%d"%(beg)
        self.rt.attributes["way"]=way

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")

class Ch(St):
    """Choose"""
    XEchoises=None
    def __init__(self,doc,rt):
        self.tp="Ch"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            self.XEchoises=self.rt.getElementsByTagName("choises")[0]
        else:
            self.XEchoises=self.doc.createElement("choises")
            self.rt.appendChild(self.XEchoises)
            self.addCho()
            
            self.init()
        
    def init(self,tar=0):
        "tar:choose for"
        self.rt.attributes["tar"]="%d"%(tar)
        
    def addCho(self):
        XEchoise=self.doc.createElement("choise")
        XEchoise.attributes["id"]="%d"%(len(self.XEchoises.childNodes))
        self.XEchoises.appendChild(XEchoise)
        choise=Cho(self.doc,XEchoise)
        choise.build()
        return XEchoise

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")      

class Cho(St):
    """Choise"""
    def __init__(self,doc,rt):
        self.tp="Cho"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("txt")):
            pass
        else:
            self.init()
        
    def init(self,txt="choice",factor="True"):
        "tar:choose for"
        self.rt.attributes["txt"]=txt
        self.rt.attributes["factor"]=factor

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")

class Jp(St):
    """Jump"""
    def __init__(self,doc,rt):
        self.tp="Jp"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("tar")):
            pass
        else:
            self.init()
        
    def init(self,tar=0,factor="True"):
        "(id:jump to,when:judge when to jump)"
        self.rt.attributes["tar"]="%d"%(tar)
        self.rt.attributes["factor"]=factor

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")

class Sp(St):
    """Special Effect"""
    def __init__(self,doc,rt):
        self.tp="Sp"
        St.__init__(self,doc,rt)
        self.build()

    def build(self):
        if(self.rt.hasAttribute("way")):
            pass
        else:
            self.init()
        
    def init(self,scr="",way=""):
        "scr:the screen that finally appear(default is nothing)\n" + \
        "   scr in ['','black','white','logo']\n" + \
        "way:the way of the effect(default is None)\n" + \
        "   way in ['','shake','flash']"
        self.rt.attributes["scr"]=scr
        self.rt.attributes["way"]=way

    def __str__(self):
        return self.rt.toxml(encoding="utf-8")
