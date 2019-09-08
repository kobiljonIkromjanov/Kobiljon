


from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
from Adafruit_CharLCD import Adafruit_CharLCD


lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()
lcd.message('   Welcome\nKobil\'s home')
sleep(2)
fnum=0

## Enrolls new finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
        lcd.clear()
        lcd.message('The given fingerprint \n sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


def Enroll():
    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')
        lcd.clear()
        lcd.message('Waiting for \n finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            lcd.clear()
            lcd.message('Template already \n exists at position ' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        lcd.clear()
        lcd.message('Remove finger...')
        sleep(2)

        print('Waiting for same finger again...')
        lcd.clear()
        lcd.message('Waiting for \n same finger again...')
        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
            lcd.clear()
            lcd.message('Fingers do \n not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        lcd.clear()
        lcd.message('Finger enrolled \n successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
def Search():
    try:
        
        lcd.clear()
        lcd.message('Waiting for \nfinger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            
            lcd.clear()
            lcd.message('No match \nfound!')
            fnum=2
	    sleep(2)
            lcd.clear()
            lcd.message('Welcome to \n Penta')
            
        else:
           
            lcd.clear()
            lcd.message('Found template \nat position #' + str(positionNumber))
            sleep(1)
            lcd.clear()
	    lcd.message('Open Door')
	    fnum=1
            sleep(2)
            lcd.clear()
	    lcd.message('Welcome to \n Penta')
        return fnum
    except Exception as e:
        exit(1)
def Delete():
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')
            lcd.clear()
            lcd.message('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)



def Fmain(con_inp):
    inp=con_inp
  
    if(inp==2):
        Enroll()
    elif(inp==1):
        fnum=Search()
    else:
        Delete()
    return fnum
#start process
if __name__ == '__main__':
   Fmain()
