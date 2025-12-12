from utime import sleep_ms
import framebuf
import loadingscreen

class LoadingScreen:
    
    def __init__(self, oled):
        self.oled = oled
        
    def buildScreen(self):
        buffer,img_res = loadingscreen.get_img()
        fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
        self.oled.fill(0)
        self.oled.show()
        self.oled.rotate(True)
        self.oled.blit(fb, 0, 0)
        self.oled.show()
        
    def destroy(self):
        self.oled.fill(0)
        #self.oled.rotate(True)
        
    def update(self):
        return