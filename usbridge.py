import select
import sys

class USBridge:
    
    #read serial communication with linux host
    def __init__(self):

        self.poll_object = select.poll()
        self.poll_object.register(sys.stdin,1)

    #poll incoming data, send back to main
    def pollInput(self):
        
        if self.poll_object.poll(0):
            payload = ""
            while(1):
                payload += sys.stdin.read(1)
                if(payload[len(payload)-1] == "\n"):
                    return payload[:-1]
        return ""