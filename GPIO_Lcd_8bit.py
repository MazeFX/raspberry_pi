# __author__ = 'MazeFX'

import RPi.GPIO as GPIO
import time

# Set pin constants
LCD_RS = 16
LCD_E  = 21
LCD_D0 = 6
LCD_D1 = 13
LCD_D2 = 19
LCD_D3 = 26
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
    GPIO.setup(LCD_D0, GPIO.OUT)
    GPIO.setup(LCD_D1, GPIO.OUT)
    GPIO.setup(LCD_D2, GPIO.OUT)
    GPIO.setup(LCD_D3, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    # Initialise the display
    lcd_init()

    while True:
        # Send text
        send_string('BREAKING', LCD_LINE_1)
        send_string('NEWS', LCD_LINE_2)

        time.sleep(3)

        move_string("Nolan zoeft", ' ', LCD_LINE_1, "van links", 'naar rechts!', LCD_LINE_2,'R')

        time.sleep(3)

def send_string(message, line):
    dif = int((LCD_WIDTH - len(message)) / 2)
    message = message.ljust(LCD_WIDTH - dif, ' ')
    message = message.rjust(LCD_WIDTH, ' ')
    lcd_string(message, line)

def move_string(message1, message2, line1, message3, message4, line2, directtion):

    arrowline1 = " --------> "
    arrowline2 = " --------> "

    S = [message1, message2, message3, message4]
    Sn = []
    for message in S:
        dif = int((LCD_WIDTH - len(message)) / 2)
        message = message.ljust(LCD_WIDTH - dif, ' ')
        message = message.rjust(LCD_WIDTH, ' ')
        Sn.append(message)

    stringline1 = Sn[0] + arrowline1 + Sn[1]
    stringline2 = Sn[2] + arrowline2 + Sn[3]
    cursor = 0

    lcd_string(Sn[0], line1)
    lcd_string(Sn[2], line2)

    time.sleep(2)
    print (' Checkpoint passed!')
    while cursor <= (len(arrowline1) + 16):
        print ('Move checkpoint passed cycle = ' + str(cursor))
        visible_message1 = stringline1[cursor: cursor +16]
        visible_message2 = stringline2[cursor: cursor +16]
        print (visible_message1)
        print (visible_message2)
        print (str(len(Sn[3])))
        print (str(len(visible_message1)))
        lcd_string(visible_message1, line1)
        lcd_string(visible_message2, line2)

        time.sleep(0.1)
        cursor += 1

def lcd_init():
    # Initialise the display
    lcd_byte(0x33, LCD_CMD) # 110011 Initialise
    lcd_byte(0x32, LCD_CMD) # 110010 Initialise
    lcd_byte(0x06, LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD) # 001100 Display On, Cursor off, blink off
    lcd_byte(0x38, LCD_CMD) # 111000 Data length, number of lines, font size FOR 8BIT
    lcd_byte(0x01, LCD_CMD) # clear display

    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte via datapins to screen
    # bits is data for characters or command
    # mode for setting command or character

    GPIO.output(LCD_RS, mode) # set the data mode

    # Send high bits
    GPIO.output(LCD_D0, False)
    GPIO.output(LCD_D1, False)
    GPIO.output(LCD_D2, False)
    GPIO.output(LCD_D3, False)
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
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D0, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D1, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D2, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D3, True)

    #Toggle the enable pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)

def lcd_string(message, line):
    # Send string to the display

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
        send_string('Goodbye!', LCD_LINE_1)
        GPIO.cleanup()
