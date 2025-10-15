import select
import sys

class USBridge:
    
    def __init__(self):
        print("class created")
        
    def read(self):
        poll_object = select.poll()
        poll_object.register(sys.stdin,1)

        if poll_object.poll(0):
           #read as character
           ch = sys.stdin.read(1)
           if(ch == "\n"):
                   print("enter pressed")
           print ('%d' %ch)
