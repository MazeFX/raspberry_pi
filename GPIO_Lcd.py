# __author__ = 'MazeFX'

import RPi.GPIO as GPIO
import time

# Set pin constants
LCD_RS = 16
LCD_E  = 21
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Set device constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# Time value constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
    #main program block

    GPIO.setmode(GPIO.BCM) # BCM mapping of GPIO pins

    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    # Initialise the display
    lcd_init()

    while True:
        # Send text
        lcd_string("Stefanie",LCD_LINE_1)
        lcd_string("is stout",LCD_LINE_2)

        time.sleep(3)

        lcd_string("is heel stout",LCD_LINE_2)

        time.sleep(3)

        lcd_string("",LCD_LINE_1)
        lcd_string("Echt waar!",LCD_LINE_2)

        time.sleep(3)

def lcd_init():
    # Initialise the display
    lcd_byte(0x33, LCD_CMD) # 110011 Initialise
    lcd_byte(0x32, LCD_CMD) # 110010 Initialise
    lcd_byte(0x06, LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD) # 001100 Display On, Cursor off, blink off
    lcd_byte(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD) # clear display

    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte via datapins to screen
    # bits is data for characters or command
    # mode for setting command or character

    GPIO.output(LCD_RS, mode) # set the data mode

    # Send high bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    #Toggle the enable pin
    lcd_toggle_enable()

    # Send low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    #Toggle the enable pin for high bits again
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)

def lcd_string(message, line):
    # Send string to the display
    dif = int((LCD_WIDTH - len(message)) / 2)
    message = message.ljust(LCD_WIDTH - dif, ' ')
    message = message.rjust(LCD_WIDTH, ' ')

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01,LCD_CMD)
        lcd_string('Goodbye!', LCD_LINE_1)
        GPIO.cleanup()
