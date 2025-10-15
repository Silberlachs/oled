class GuiBuilder:
    
    def __init__(self, oled, strings):
        self.oled 		= oled
        self.strings 	= strings
        
    def showArgs(self):
        print(self.strings)