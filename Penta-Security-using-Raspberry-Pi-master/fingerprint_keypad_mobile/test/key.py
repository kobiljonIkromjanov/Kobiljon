
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()
lcd.message('   Welcome\nKobil\'s home') 
keys=[1]
keyStr=''


MATRIX = [[1, 2, 3, 'A'],
          [4, 5, 6, 'B'],
          [7, 8, 9, 'C'],
          ['*', 0, '#', 'D']]

ROW = [4,17,27,22]
COL = [12,16,20,21]
list=[]
key=[]

errchar=''
data=0
finish=0

        

for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j],1)

for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN,  pull_up_down=GPIO.PUD_UP)
       

try:
        finish=0
        while(finish<1):
                for j in range (4):
                        GPIO.output(COL[j],0)

                        for i in range (4):
                                if GPIO.input(ROW[i])==0:
                                        data=MATRIX[i][j]

                                        
                                        
                                        if data=='C':
                                                list=[]
                                                                                       
                                        elif data=='D':
                                                if len(list)>0:
                                                        list.pop()
                                                if len(list)==0:
                                                        list=[]
                                                
                                                
                                        elif data=='A' or data=='B' or data=='*' or data=='#':
                                                errchar=data
                                                                                               

                                        else:
                                                list.append(data)                                 
                                                
                                                if len(list)==4:                                                        
                                                        finish=1
                                        keyStr=str(list)
                                        keyStr=keyStr[1 :-1]
                                        lcd.clear()
                                        lcd.message('Input key:\n')
                                        lcd.message(keyStr)
                                        

                                        while(GPIO.input(ROW[i])==0): #to stop after one input from keypad
                                                pass
                        GPIO.output(COL[j],1)
                        
except KeyboardInterrupt:
        GPIO.cleanup()
        lcd.clear()
finally:
        lcd.clear()
