#coding:gbk
import os,sys
sys.path.insert(0,os.path.join(os.path.abspath("."),"src"))
import settings
settings.setAppPath(".")
from avgbase import *
import saveload
def main():
    while True:
        print "==========   �浵ͳ��   =========="
        d=saveload.ldread()
        cg=0
        for i in d.cgs:
            if i:
                cg+=1
        cg_rate=cg*1.0/(len(d.cgs)-1)*100
        bar='['+int(cg_rate/2)*'|'+(50-int(cg_rate/2))*'-'+']'
        print "%15s %s %0.1f%%"%("CG�ռ��ʣ�",bar,(cg_rate))
        st=0
        stsum=0
        for pl in d.plots:
            for i in pl:
                if i:
                    st+=1
            stsum+=len(pl)
        st_rate=st*1.0/stsum*100
        bar='['+int(st_rate/2)*'|'+(50-int(st_rate/2))*'-'+']'
        print "%15s %s %0.1f%%"%("��������ʣ�",bar,(st_rate))
        print
        raw_input("���»س�ˢ��")
if __name__=="__main__":
    main()
