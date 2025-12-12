import framebuf
from LoadingScreen import LoadingScreen
import logo
from utime import sleep_ms

class GuiBuilder:
    
    def __init__(self, oled):
        self.oled 		= oled
        self.nameStr 	= "Birdflip Studios "
        self.conStr 	= "Connected !"
        #self.test 		= "ASDFGHHJKLÖ"
        self.loadingScreen = LoadingScreen(self.oled)
        
    def showLogo(self):
        buffer,img_res = logo.get_img()
        fb = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
        self.oled.rotate(False)
        self.oled.blit(fb, 0, 0)
        self.oled.show()
        
        #draw parrot and move it to the left
        for x in range(0,100):
            self.oled.scroll(-1, 0)
            self.oled.show()
            sleep_ms(10)
           
        #delete screen
        sleep_ms(100)
        self.oled.fill(1)
        self.oled.show()
        
        #print out our proud name of birdflip, greatest of all studios
        for charCount in range(0,len(self.nameStr)):
            self.oled.text(self.nameStr[:charCount],0,32,0)
            sleep_ms(50)
            self.oled.show()
            
        sleep_ms(2000)
        self.oled.fill(0)

    def showLoadingScreen(self):
        self.loadingScreen.buildScreen()
        
    def showConMsg(self):
        #delete screen
        self.oled.fill(0)
        self.oled.rotate(False)
        self.oled.show()
        sleep_ms(30)
        
        for charCount in range(0,len(self.conStr)):
            self.oled.text(self.conStr[:charCount],24,32,1)
            sleep_ms(50)
            self.oled.show()
            
        #flash message
        for flash in range(0,4):
            sleep_ms(200)
            self.oled.contrast(0)
            sleep_ms(200)
            self.oled.contrast(128)
            
    def drawSystemHUD(self):
        self.oled.rotate(False)
        self.oled.fill(0)
        
        #draw upper block
        self.oled.hline(0, 0, 9, 1)
        self.oled.hline(0, 1, 9, 1)
        self.oled.hline(0,2,9,1)
        self.oled.hline(0,3,9,1)
        self.oled.hline(0, 4, 9, 1)
        self.oled.hline(0, 5, 9, 1)
        self.oled.hline(0, 6, 9, 1)
        
        self.oled.text("TEMP",10,0,1)
        
        #draw lower block
        self.oled.hline(0, 34, 9, 1)
        self.oled.hline(0, 35, 9, 1)
        self.oled.hline(0,36,9,1)
        self.oled.hline(0,37,9,1)
        self.oled.hline(0, 38, 9, 1)
        self.oled.hline(0, 39, 9, 1)
        self.oled.hline(0, 40, 9, 1)
        
        self.oled.text("RAM",10,34,1)
        
        self.oled.show()
        return
    
    def addEntries(self, names):
        lineMultiplyer = 8
        for x in range(0,len(names)):
            self.oled.text("|"+names[x],0,8 + lineMultiplyer * x,1)
        self.oled.show()
        return
    
    #hardcoded, add generic value engine
    def updateValues(self,values):
        
        self.oled.text(str(values[0]) + "C",100,8,1)
        self.oled.text(str(values[1]) + "C",100,16,1)
        self.oled.text(str(values[2]) + "C",100,24,1)
        
        total = values[3] / 1000000
        available = values[4] / 1000000
        
        self.oled.text("[" + str(round(total - available,2)) + "/" + str(round(total,2)) + "]",0,44,1)
        
        #get percentage number
        percentage = 100 - round(available / total *100)
        self.oled.text(str(percentage) + "%", 100, 44,1)
        
        #draw RAM gauge
        #self.oled.vline(12,54,9,1)
        self.oled.vline(13,55,8,1)
        self.oled.hline(14,55,100,1)
        self.oled.hline(14,55,percentage,1)
        self.oled.hline(14,56,percentage,1)
        self.oled.hline(14,57,percentage,1)
        self.oled.hline(14,58,percentage,1)
        self.oled.hline(14,59,percentage,1)
        self.oled.hline(14,60,percentage,1)
        self.oled.hline(14,61,percentage,1)
        self.oled.hline(14,62,100,1)
        self.oled.vline(114,55,8,1)
        #self.oled.vline(116,54,9,1)
        
        #finally, update
        self.oled.show()
     
    def refreshDisplayValue(self):
        #refresh ram display
        for x in range(0,8):
            self.oled.hline(0,44+x,128,0)
            
        #refresh temperature data
        for x in range(100,128):
            self.oled.vline(x,0,32,0)
            
        #refresh gauge
        self.oled.hline(14,56,100,0)
        self.oled.hline(14,57,100,0)
        self.oled.hline(14,58,100,0)
        self.oled.hline(14,59,100,0)
        self.oled.hline(14,60,100,0)
        self.oled.hline(14,61,100,0)
