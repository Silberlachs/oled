import framebuf
from LoadingScreen import LoadingScreen
import imageLib
from utime import sleep_ms

class GuiBuilder:
    
    def __init__(self, oled, contrast):
        self.oled 			= oled
        self.nameUpper 		= "Renraku"
        self.nameUnder  	= "Computersystems"
        self.conStr 		= "Connected !"
        self.animationCycle = "waiting"
        self.screenContrast = contrast
        self.displayOrder 	= []
        self.initialized 	= False
        self.loadingScreen 	= LoadingScreen(self.oled)
      
    #used for animations during wait time
    def setAnimationCycle(self,cycle):
        self.animationCycle = cycle
        
    def showLogo(self):
        buffer,img_res = imageLib.get_parrot()
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
        
        #show "studio name"
        for charCount in range(0,len(self.nameUpper) +1):
            self.oled.text(self.nameUpper[:charCount],32,10,0)
            sleep_ms(50)
            self.oled.show()
            
        for charCount in range(0,len(self.nameUnder) +1):
            self.oled.text(self.nameUnder[:charCount],4,32,0)
            sleep_ms(50)
            self.oled.show()
            
        sleep_ms(2000)
        self.oled.fill(0)

    def showLoadingScreen(self):
        self.loadingScreen.buildScreen()
        
    def update(self):
        # unfortunately, no "match" support as of january 2026
        if(self.animationCycle == "waiting"):
            self.loadingScreen.update()
        
        #if(self.animationCycle == "running"):
        #    print("im running")
            
        return

        
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
            sleep_ms(100)
            self.oled.contrast(0)
            sleep_ms(100)
            self.oled.contrast(self.screenContrast)
            
    def drawSystemHUD(self, payload):
        self.displayOrder = payload	#used to refresh values later
        self.oled.rotate(False)
        self.oled.fill(0)
        
        #leave 1 px between lines or letters will bleed into each other
        lineMultiplier = 9
        currentLine = 0
        
        for x in range(0,len(payload)):
            if "$:" in payload[x]:
                section = payload[x].split(":")[1]
                name = section.split(",")[0]

                #draw block of 8 px
                self.oled.hline(0, currentLine,   9, 1)
                self.oled.hline(0, currentLine+1, 9, 1)
                self.oled.hline(0, currentLine+2, 9, 1)
                self.oled.hline(0, currentLine+3, 9, 1)
                self.oled.hline(0, currentLine+4, 9, 1)
                self.oled.hline(0, currentLine+5, 9, 1)
                self.oled.hline(0, currentLine+6, 9, 1)
        
                self.oled.text(name,10,currentLine,1)
                currentLine += lineMultiplier
                continue
        
            if "&:" in payload[x]:
                continue	##implement gauge
        
            self.oled.text("|" + payload[x].replace("_",""),0, currentLine , 1)
            currentLine += lineMultiplier
        
        self.initialized = True
        self.oled.show()
        return
    
    #hardcoded
    def updateValues(self,values):
        
        if self.initialized == False:
            return
        
        self.oled.text(values[0] + "C",100,8,1)
        self.oled.text(values[1] + "C",100,16,1)
        self.oled.text(values[2] + "C",100,24,1)
        
        ramOffset = self.displayOrder.index(" ")
        ramOffset = ramOffset * 9
        try:
            total = int(values[3]) / 1000000
            available = int(values[4]) / 1000000
            self.oled.text("[" + str(round(total - available,2)) + "/" + str(round(total,2)) + "]",0,ramOffset,1)
            
            #get percentage number
            percentage = 100 - round(available / total *100)
            self.oled.text(str(percentage) + "%", 100, ramOffset,1)
            
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
        except:
            self.oled.text("input error", 0 ,ramOffset ,1)
        
        #finally, update
        self.oled.show()
            
     
    def refreshDisplayValues(self):
            
        #refresh temperature data (always at x=100)
        for x in range(100,128):
            self.oled.vline(x,0,32,0)
         
        #refresh ram display, needs to be updated for other projects
        ramOffset = self.displayOrder.index(" ")
        ramOffset = ramOffset * 9
        for x in range(0,8):
            self.oled.hline(0,ramOffset + x,128,0)
        
        self.oled.hline(14 ,55 ,100 ,0)
        self.oled.hline(14 ,56 ,100 ,0)
        self.oled.hline(14 ,57 ,100 ,0)
        self.oled.hline(14 ,58 ,100 ,0)
        self.oled.hline(14 ,59 ,100 ,0)
        self.oled.hline(14 ,60 ,100 ,0)
        self.oled.hline(14 ,61 ,100 ,0)
