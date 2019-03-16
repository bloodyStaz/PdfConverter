import sys
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
import time
import shutil

class MyThread(QThread):
    signal=pyqtSignal(str)
    def __init__(self,fileOptionState,file,logoState=None,logoPath=None,delay=10):
        super(QThread,self).__init__()
        self.fileOptionState=fileOptionState
        self.filePath=file
        self.logoState=logoState
        self.logoPath=logoPath
        self.delay=delay
    def run(self):
        self.signal.emit("Please Wait while we ready you video")
        self.clean()
        if self.fileOptionState==1:
            self.pdfConvert(self.filePath)
            self.vidConvert(self.delay)
        elif self.fileOptionState==2:
            self.imgConvert(self.filePath)
            self.vidConvert(self.delay)
        elif self.fileOptionState==3:
            self.convert(self.filePath)
        self.signal.emit("Done")

    def clean(self):
        for f in os.listdir("tmp/"):
            os.remove("tmp/" + f)

    def pdfConvert(self,filePath):

        pdfToImg = ("include/poppler/bin/pdftoppm.exe")
        pdf = '"{}"'.format(filePath)
        process = subprocess.Popen('"%s" -png %s tmp/out' % (pdfToImg, pdf),stdout=subprocess.PIPE)
        process.wait()
    def imgConvert(self,filePath):
        j = 00
        for i in filePath:
            shutil.copyfile(i, "tmp/out-" + str(j) + ".png")
            j = j + 1
    def convert(self,filePath):
        #print(,type(filePath))
        process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i include/logo.png -filter_complex \
"overlay=W-w-5:H-h-5" \
-codec:a copy {}'.format(str(filePath)[2:-2:], "tmp/tmp2.mp4"),stdout=subprocess.PIPE)
        process.wait()

        if(self.logoState !="Upload Logo"):
            if(self.logoState=="Top Left"):
                print("adding top left logo")
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.logoState=="Top Right"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=W-w-5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.logoState=="Bottom Left"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:H-h-5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()


            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp3.mp4", "tmp/tmp4.mp4"))
            process.wait()

        else:
            print("in else condtion")
            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp2.mp4", "tmp/tmp4.mp4"))
            process.wait()


    def vidConvert(self,delay):
        #video = '"{}/{}.mp4"'.format(self.txtBox2.text(), self.txtBox3.text())
        res = "1920:1080"
        images = []
        delay=self.delay

        framelength = delay + 1
        for img in os.listdir("tmp\\"):
            if img.endswith(".png") or img.endswith(".jpg"):
                images.append(img)
        loop = ""
        for f in images:
            imgPath = os.path.join("tmp\\", f)
            loop += "-loop 1 -t {} -i {} ".format(framelength, imgPath)

        effect = ""
        lst = "[v0]"
        for i in range(1, len(images)):
            lst += "[v{}]".format(i)
            effect += '[{0}:v]scale={1}:force_original_aspect_ratio=decrease,pad={1}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st={2}:d=1[v{0}];'.format(
                i, res, delay)
            
        process = subprocess.Popen('include\\ffmpeg\\bin\\ffmpeg.exe -y  \
        {} \
        -filter_complex \
        "[0:v]scale={}:force_original_aspect_ratio=decrease,pad={}:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=out:st={}:d=1[v0]; \
        {} \
        {} \
        concat=n={}:v=1:a=0,format=yuv420p[v]" -map "[v]" {}'.format(loop, res, res, delay, effect, lst, len(images), "tmp/tmp1.mp4"))
        process.wait()

        process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i include/logo.png -filter_complex \
"overlay=W-w-5:H-h-5" \
-codec:a copy {}'.format("tmp/tmp1.mp4", "tmp/tmp2.mp4"))
        process.wait()

        if(self.logoState !="Upload Logo"):
            if(self.logoState=="Top Left"):
                print("adding top left logo")
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.logoState=="Top Right"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=W-w-5:5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()
            if(self.logoState=="Bottom Left"):
                process=subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -i {} -filter_complex \
                        "overlay=5:H-h-5" -codec:a copy {}'.format("tmp/tmp2.mp4",self.logoPath,"tmp/tmp3.mp4"))
                process.wait()


            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp3.mp4", "tmp/tmp4.mp4"))
            process.wait()

        else:
            print("in else condtion")
            process = subprocess.Popen('include/ffmpeg/bin/ffmpeg.exe -i {} -c:v libx264 -profile:v high -vf scale=1920:1080 -r 25 {}'.format("tmp/tmp2.mp4", "tmp/tmp4.mp4"))
            process.wait()

class ProgressThread(QThread):
    progressSignal=pyqtSignal(str)
    def run(self):
        while True:
            self.progressSignal.emit("Please Wait while we ready you video.")
            self.progressSignal.emit("Please Wait while we ready you video..")
            self.progressSignal.emit("Please Wait while we ready you video...")
        
    

    