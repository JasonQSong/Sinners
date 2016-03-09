##region:settings:
font="font.ttf"
fullscreen=False#True
fadeoutms=1000
##endregion

wait=False
waitforchoose=False
mode=0
delay_char=70
delay_sentence=300
auto=True
skipping=False
pause=True
onlypic=False

apppath=".."
fontpath="..\\font"
imgpath="..\\img"
bgmpath="..\\bgm"
wavpath="..\\wav"
savepath="..\\save"
seenpath="..\\seen"
def setAppPath(path):
    import os
    global apppath
    apppath=path
    global fontpath,imgpath,bgmpath,wavpath,savepath,seenpath
    fontpath=os.path.join(apppath,"font")
    imgpath=os.path.join(apppath,"img")
    bgmpath=os.path.join(apppath,"bgm")
    wavpath=os.path.join(apppath,"wav")
    savepath=os.path.join(apppath,"save")
    seenpath=os.path.join(apppath,"seen")
