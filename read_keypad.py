import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

L1 = 12
L2 = 16
L3 = 20
L4 = 21

C1 = 6
C2 = 13
C3 = 19
C4 = 26

LAST_KEY_TIMEOUT = timedelta(seconds = 1)

def init_keypad():
    # Initialize the GPIO pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    ret_char = None
    if(GPIO.input(C1) == 1):
        ret_char = characters[0]
    if(GPIO.input(C2) == 1):
        ret_char = characters[1]
    if(GPIO.input(C3) == 1):
        ret_char = characters[2]
    if(GPIO.input(C4) == 1):
        ret_char = characters[3]
    GPIO.output(line, GPIO.LOW)
    return ret_char

def read_lines():
    # call the readLine function for each row of the keypad
    # if valid return, save it
    ret_char = None
    temp_char = readLine(L1, ["1","2","3","A"])
    if temp_char:
        ret_char = temp_char
    temp_char = readLine(L2, ["4","5","6","B"])
    if temp_char:
        ret_char = temp_char
    temp_char = readLine(L3, ["7","8","9","C"])
    if temp_char:
        ret_char = temp_char
    temp_char = readLine(L4, ["*","0","#","D"])
    if temp_char:
        ret_char = temp_char

    return ret_char

def receive_thread( queue ):
    last_key = None
    last_key_time = 0
    init_keypad()
    try:
        while True:
            time.sleep(0.1)
            ret_char = read_lines()
            if ret_char:

                # Debounce the input more
                if ret_char == last_key and ( datetime.now() - last_key_time ) < LAST_KEY_TIMEOUT:
                    continue
                last_key = ret_char
                last_key_time = datetime.now()

                queue.put( ret_char )
    except KeyboardInterrupt:
        print("\nApplication stopped!")