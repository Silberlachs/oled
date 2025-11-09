import framebuf
import logo
from utime import sleep_ms

class GuiBuilder:
    
    def __init__(self, oled, strings):
        self.oled 		= oled
        self.strings 	= strings
        self.nameStr 	= "Birdflip Studios "
        
    def showArgs(self):
        print(self.strings)
        
    def showLogo(self):
        buffer,img_res = logo.get_img()
        fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
        self.oled.rotate(True)
        self.oled.blit(fb, 0, 0)
        for x in range(0,100):
            self.oled.scroll(1, 0)
            self.oled.show()
            sleep_ms(10)
           
        sleep_ms(250)
        self.oled.fill(1)
        self.oled.show()
        self.oled.rotate(False)
        
        for charCount in range(0,len(self.nameStr)):
            self.oled.text(self.nameStr[:charCount],0,32,0)
            sleep_ms(50)
            self.oled.show()
            
        sleep_ms(2000)
        self.oled.fill(0)
