import time

LCD_WIDTH = 16
LCD_LINE_1 = 1
LCD_LINE_2 = 2

def move_string(message1, message2, line1, message3, message4, line2, directtion):

    arrowline1 = " --------\ "
    arrowline2 = " --------/ "

    S = [message1, message2, message3, message4]
    Sn = []
    for message in S:
        print (message)
        print (str(len(message)))
        dif = int((LCD_WIDTH - len(message)) / 2)
        message = message.ljust(LCD_WIDTH - dif, ' ')
        message = message.rjust(LCD_WIDTH, ' ')
        Sn.append(message)
        print (message)

    stringline1 = Sn[0] + arrowline1 + Sn[1]
    stringline2 = Sn[2] + arrowline2 + Sn[3]
    cursor = 0

    print (Sn[0])
    print (Sn[2])

    time.sleep(1)
    
    while cursor <= (len(arrowline1) + 16):
        print ('cursor = ' + str(cursor))
        visible_message1 = stringline1[cursor - 1: cursor +15]
        visible_message2 = stringline2[cursor - 1: cursor +15]
        print ('length = ' + str(len(visible_message1)))
        print (visible_message1)
        print (visible_message2)

        time.sleep(0.005)
        cursor += 1
        
if __name__ == '__main__':

    try:
        move_string("Nolan zoeft", ' ', LCD_LINE_1, "van links", 'naar rechts!', LCD_LINE_2,'R')
    except KeyboardInterrupt:
        pass
        
