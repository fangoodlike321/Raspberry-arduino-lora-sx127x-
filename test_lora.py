from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from urllib import parse,request
import json
import time
import picamera
import requests

url='http://sunhaojie.applinzi.com/post.php'


def sendMsgHT(x,y):
    textmod = {"tem":y,
                "hum":x
                }
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent':'Mozilla/5.0(Windows NT 6.1; Trident/7.0;rv:11.0)like Gecko',"Content-Type":"application/json"}
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    print(res)
    print(res.decode(encoding='utf-8'))
def sendImage():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        for filename in camera.capture_continuous('img.jpg'):
            print('Captured %s' % filename)
            time.sleep(0.02) # 休眠5分钟
            url='http://sunhaojie.applinzi.com/picture.php'
            files = {'baimafeima': open('img.jpg', 'rb')}
            req = requests.post(url=url,files=files)
            print(req.text)
def getOrder():
    req = request.Request(url="http://sunhaojie.applinzi.com/info.php")
    res = request.urlopen(req)
    res = res.read()
    return res.decode(encoding='utf-8')
class LoRaRcvCont(LoRa): #recieve data from lora
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)#initialise DIO0 for rxdone  

    def on_rx_done(self):
        #BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)          #read data
        temp = str.split(bytes(payload).decode())
        print(temp)
        if temp[0] =='BADD':
            if(temp[1] == 'HT'):
                sendMsgHT(temp[2],temp[3])
                #print("YES")
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        #BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        counter = 5;
        while counter:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
            counter = counter - 1;
        time.sleep(5)
class LoRaBeacon(LoRa):

    def __init__(self, verbose=False):
        super(LoRaBeacon, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        lora.set_pa_config(pa_select=1)
        self.set_dio_mapping([1,0,0,0,0,0])

    def on_rx_done(self):
        print("\nRxDone")
        print(self.get_irq_flags())
        print(map(hex, self.read_payload(nocheck=True)))
        #elf.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self,Lora_message):
        global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        if args.single:
            print
            sys.exit(0)
        #BOARD.led_off()
        sleep(args.wait)
        self.Lora_message=Lora_message
        rawinput = self.Lora_message
        data = [int(hex(ord(c)), 0) for c in rawinput]
        #self.write_payload([0x0f])
        self.write_payload(data)
        #BOARD.led_on()
        self.set_mode(MODE.TX)

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        global args
        sys.stdout.write("\rstart")
        self.write_payload([0x0f])
        self.set_mode(MODE.TX)
        while True:
            sleep(1)
def Lora_GetMessage(x):
    lora.set_mode(MODE.STDBY)
    lora.start()
    lora.set_mode(MODE.SLEEP)
    #BOARD.teardown()
def Lora_SendMessage(lora,Lora_message):
    lora.set_mode(MODE.STDBY)
    lora.start()
    lora.set_mode(MODE.SLEEP)

if __name__ == '__main__':
    BOARD.setup()
    temp = 1;
    temp1 = 1;
    while True:
        if getOrder() == True:
            if temp1 ==1:
                BOARD.setup()
                parser = LoRaArgumentParser("A simple LoRa beacon")
                parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
                parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")
                lora = LoRaBeacon(verbose=False)
                args = parser.parse_args(lora)
                lora.set_pa_config(pa_select=1)
                Lora_mess = getOrder()
                Lora_SendMessage (lora1,Lora_mess)
                temp1 = temp1+1;
            else:
                Lora_mess = getOrder()
                Lora_SendMessage (lora1,Lora_mess)
        else:
            if temp ==1:
                BOARD.setup()
                parser = LoRaArgumentParser("Continous LoRa receiver.")
                lora = LoRaRcvCont(verbose=False)
                args = parser.parse_args(lora)
                lora.set_pa_config(pa_select=1)
                lora.set_freq(411)
                Lora_GetMessage(temp)
                temp = temp + 1;
            else:
                Lora_GetMessage(lora)
                time.sleep(1)
