import web
import json
import serial

ser = serial.Serial('/dev/ttyACM0', 57600,timeout=1)#RasPi
#ser = serial.Serial('/dev/cu.usbmodemfd131', 57600,timeout=1)#imac
#ser = serial.Serial('/dev/cu.usbmodem1a21', 9600,timeout=1)#macbook

def notfound():
    #return web.notfound("Sorry, the page you were looking for was not found.")
    return json.dumps({'ok':0, 'errcode': 404})

def internalerror():
    #return web.internalerror("Bad, bad server. No donut for you.")
    return json.dumps({'ok':0, 'errcode': 500})

def getSerial():
    #ser.flushInput()
    buffer = ser.read(ser.inWaiting())#read whole buffer
    buffer = buffer.split('\r\n')[-3:-2]#second last complete data element from buffer
    print(float(buffer[0])*1000)#debug console
    return json.dumps({'vekt': abs(int(1000 * float(buffer[0]))) })#generate json reply

urls = (
   '/scale(.*)', 'handleRequest',
   # '/(.*)', 'handleRequest'
   )

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror


class handleRequest:
    def GET(self, method_id):
        if not method_id: 
            return web.notfound()
        else:
            return getSerial()

    def POST(self):
        i = web.input()
        data = web.data() # you can get data use this method
        print data
        pass

if __name__ == "__main__":
    app.run()
