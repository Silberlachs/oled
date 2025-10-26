import select
import sys

class USBridge:
    
    def __init__(self):
        print("class created")
        self.input = ""
        self.button = ""
        self.flushbuffer = 0
        self.poll_object = select.poll()
        self.poll_object.register(sys.stdin,1)
        
    def read(self):
        
        if self.poll_object.poll(0):
            self.button = sys.stdin.read(1)

            if(self.button == "\n"):
                if(self.flushbuffer < 1):
                    self.flushbuffer += 1
                    return ""
                else:
                    payload = self.input
                    self.flushbuffer = 0
                    self.input = ""
                    return payload
                
            self.input += self.button
        return ""
