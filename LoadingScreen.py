from utime import sleep_ms
import framebuf
import imageLib

class LoadingScreen:
    
    def __init__(self, oled):
        self.oled = oled
        self.parrotBuff = []
        self.parrotRes = []
        self.frameCounter = 0
        
    def buildScreen(self):
        buffer,img_res = imageLib.get_loadingScreen()
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
        if(self.frameCounter < 16):
            self.frameCounter += 1
        else:
            self.frameCounter = 1
         
        funcName = "get_birb" + str(self.frameCounter)
        birbFunc = getattr(imageLib, funcName)
        self.parrotBuff, self.parrotRes = birbFunc()
        fb = framebuf.FrameBuffer(self.parrotBuff, self.parrotRes[0], self.parrotRes[1], framebuf.MONO_HMSB)
        self.oled.blit(fb, 50, 10)
        self.oled.show()
        return