from utime import sleep_ms
from random import randint
import framebuf
import imageLib

class LoadingScreen:
    
    def __init__(self, oled):
        self.oled = oled
        self.parrotBuff 	= []
        self.cloudBuff 		= []
        self.cityBuff		= []
        
        self.parrotRes 		= []
        self.cloudRes		= []
        self.cityRes		= []
        
        self.particles 		= []
        self.cityTilePos	= [144, 129, 113, 97, 81, 65, 49, 33, 17, 1, -15, -24]	#random values

        self.cloudPos 		= 15
        self.frameCounter 	= 0
        
    def buildScreen(self):
        buffer,img_res = imageLib.get_loadingScreen()
        header = framebuf.FrameBuffer(buffer, img_res[0], img_res[1], framebuf.MONO_HMSB)
        self.oled.fill(0)
        self.oled.show()
        self.oled.rotate(True)
        self.oled.blit(header, 0, 0)
        self.oled.show()
        
        #initialize cloud and city here, image never changes
        self.cloudBuff, self.cloudRes 	= imageLib.get_cloud()
        self.cityBuff, self.cityRes 	= imageLib.get_city()
        self.cloud 	= framebuf.FrameBuffer(self.cloudBuff, self.cloudRes[0], self.cloudRes[1], framebuf.MONO_HMSB)
        self.city 	= framebuf.FrameBuffer(self.cityBuff, self.cityRes[0], self.cityRes[1], framebuf.MONO_HMSB)
        
    def destroy(self):
        self.oled.fill(0)
    
    # we create a simple particle system
    def spawnParticle(self):
        num = randint(12,30)
        self.particles.append([0,num])
   
    def spawnCityTile(self):
        self.cityTilePos.append(-24)
    
    def updateObjects(self):
        for particle in self.particles:
            self.oled.hline(particle[0],particle[1],16,0)
            #self.oled.hline(particle[0],particle[1]+1,8,0)
            particle[0] += 10
            self.oled.hline(particle[0],particle[1],16,1)
            #self.oled.hline(particle[0],particle[1]+1,8,1)
            
            if(particle[0] > 128):
                self.particles.remove(particle)
                
        self.cloudPos 	= self.cloudPos + 1
        self.oled.blit(self.cloud, self.cloudPos, 40)
        
        #we want only 1 for loop to save some cpu time
        for count in range(0,len(self.cityTilePos)-1):
            self.cityTilePos[count] += 2
            self.oled.blit(self.city, self.cityTilePos[count], 0)
            if(self.cityTilePos[count] > 150):
               del self.cityTilePos[0]
            
        if(self.cloudPos > 128):
            self.cloudPos = -20
            
        self.oled.show()      
    
    #update the whole loading screen animations
    def update(self):
        if(self.frameCounter < 16):
            self.frameCounter += 1
        else:
            self.frameCounter = 1
            self.spawnParticle()
            
        if(self.frameCounter % 8 == 0):
            self.spawnCityTile()
       
        funcName = "get_birb" + str(self.frameCounter)
        birbFunc = getattr(imageLib, funcName)
        self.parrotBuff, self.parrotRes = birbFunc()
        parrot 	= framebuf.FrameBuffer(self.parrotBuff, self.parrotRes[0], self.parrotRes[1], framebuf.MONO_HMSB)

        self.oled.blit(parrot, 50, 10)
        
        self.updateObjects()
        self.oled.show()
        return