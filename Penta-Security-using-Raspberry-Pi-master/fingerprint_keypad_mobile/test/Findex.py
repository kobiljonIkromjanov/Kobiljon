#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
from Adafruit_CharLCD import Adafruit_CharLCD
from pyfingerprint.pyfingerprint import PyFingerprint
from time import sleep

## Shows the template index table
##
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()
lcd.message('   Welcome\nKobil\'s home')
sleep(2)
## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
        lcd.message('The given fingerprint sensor password is wrong!')
        sleep(1)

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to show a template index table page
try:
    page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
    page = int(page)

    tableIndex = f.getTemplateIndex(page)

    for i in range(0, len(tableIndex)):
        print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
