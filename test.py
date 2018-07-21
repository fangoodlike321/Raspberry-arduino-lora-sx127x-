#!/usr/bin/env python3


import datetime
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from urllib import parse,request
import json
import time
import picamera
import requests
import subprocess
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.application import MIMEApplication
import threading

url='******************'
receiver= "**********"  #Email Alram ,just input the Email you want send
sender = "*********"  
pwd= "*********"
def SomeOne_timer(): #timer,make send email period
    global SomeFlag
    SomeFlag =SomeFlag  + 1
def Fire_timer():
    global FireFlag
    FireFlag =FireFlag + 1
def sendMsgHT(x,y):          #tempture send to PHP
    textmod = {"tem":y,
                "hum":x
                }
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent':'Mozilla/5.0(Windows NT 6.1; Trident/7.0;rv:11.0)like Gecko',"Content-Type":"application/json"}
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    
def sendVideo(filename):                              #send video to PHP server
    with picamera.PiCamera() as camera:
        filename = str(filename)
        camera.resolution = (640, 480)
        camera.start_recording(filename+'.h264')
        camera.wait_recording(5)
        camera.stop_recording()
        time.sleep(0.5)
        subprocess.Popen("MP4Box -add {0}.h264 {1}.mp4".format(filename, filename), shell= True)
        time.sleep(0.5)
        subprocess.Popen("rm {0}.h264".format(filename), shell= True)
        url=*********************'
        files = {'baimafeima': open(filename+'.mp4', 'rb')} #baimafeima is a key which you should define in order to send to php
        req = requests.post(url=url,files=files)
        print(req.text)
def sendWarining(text1,text2):     #Email 
    msg = MIMEMultipart()
    msg["Subject"] =text1     #邮件的主题
    msg["From"] = sender  
    msg["To"] = receiver
    part = MIMEText(text2) #邮件的正文  
    msg.attach(part)
    try:
        s = smtplib.SMTP("smtp.163.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25 
        s.ehlo()  
        s.starttls()  
        s.login(sender, pwd)  # 登陆服务器  
        s.sendmail(sender, receiver, msg.as_string())  # 发送邮件  
        s.close()  
        print('邮件发送成功！')
    except smtplib.SMTPException:  
        print('邮件发送失败！')
    return 0
def getOrder():                               #get order from PHP server
    req = request.Request(url="**************************")
    res = request.urlopen(req)
    res = res.read()
    print(res)
    return res.decode(encoding='utf-8')
class LoRaRcvCont(LoRa): #recieve data from lora
    def __init__(self): #初始化函数
        super(LoRaRcvCont, self).__init__(False)
        self.set_mode(MODE.SLEEP)     #设置sleep以便对寄存器操作(make mode sleep to control the reg..)
        self.set_dio_mapping([1,0,0,0,0,0]) #设置dio1口
    def startSend(self,msg):                  #send tp lora
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        rawinput = msg
        data = [int(hex(ord(c)), 0) for c in rawinput]
        count1 = 5
        while count1:
            self.write_payload(data)
            self.set_mode(MODE.TX)
            count1 = count1-1
            sleep(0.2)
            print(data)
    def startRec(self):                      #lora recieve data from ardrunio
        count = 5
        while count:
            sleep(.2)
            self.clear_irq_flags(RxDone=1)
            payload = self.read_payload(nocheck=True)
            print(bytes(payload).decode())
            temp = bytes(payload).decode()
            if temp == "someone"and EmailFlag ==1:
                if if SomeBefore == SomeFlag and EmailFlag ==1:
                    sendWarining("有人闯入","请打开微信小程序查看监控")
                    global SomeBefore
                    SomeBefore = SomeBefore + 1
                    timer = threading.Timer(300,SomeOne_timer)
                    timer.start()
                    break
            elif temp == '':
                time.sleep(0.1)
            elif temp =='fire':
                if FireBefore == FireFlag:
                    sendWarining("烟雾传感器报警","请打开微信小程序查看情况")
                    global FireBefore
                    FireBefore = FireBefore + 1
                    timer = threading.Timer(300,Fire_timer)
                    timer.start()
                    break
            else:
                temp = str.split(temp)
                sendMsgHT(temp[1],temp[2])
                break
            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) 
            count = count - 1
if __name__ == '__main__':
    global EmailFlag
    BOARD.setup()                                #open SPI  and other GPIO
    lora = LoRaRcvCont()
    lora.set_pa_config(pa_select=1)
    lora.set_freq(366)                           #set freqency 
    videoName = 1
    global FireBefore,FireFlag 
    FireBefore,FireFlag = 1,1
    global SomeBefore,SomeFlag
    SomeBefore,SomeFlag = 1,1
    while True:
        print(FireFlag)
        time.sleep(0.5)
        temp = getOrder()
        print("THIS 1",temp)
        if temp == "NUL":                    
            lora.startRec()
        elif temp =="coo":
            if videoName == 6:
                videoName = 1
            else :
                sendVideo(videoName)
                videoName= videoName + 1
        elif temp =='so':
            lora.startSend(temp)
            EmailFlag = 1
        elif temp =='sf':
            EmailFlag = 0
        else :
            lora.startSend(temp)	    
            time.sleep(0.5)
