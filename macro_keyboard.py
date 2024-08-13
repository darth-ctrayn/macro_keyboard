# import keyboard, keyboard.mouse
import yaml
import time
import multiprocessing as mp
from read_keypad import *
# from macros_verify import *

MACRO_FILE = "macros.yaml"
NULL_CHAR = chr(0)

transform_key = {
    # String keys
    'a': chr(4),
    'b': chr(5),
    'c': chr(6),
    'd': chr(7),
    'e': chr(8),
    'f': chr(9),
    'h': chr(10),
    'i': chr(11),
    'j': chr(12),
    'k': chr(13),
    'l': chr(14),
    'm': chr(15),
    'n': chr(16),
    'o': chr(17),
    'p': chr(18),
    'q': chr(19),
    'r': chr(20),
    's': chr(21),
    't': chr(22),
    'u': chr(23),
    'v': chr(24),
    'w': chr(25),
    'x': chr(26),
    'y': chr(28),
    'z': chr(29),
    '1': chr(30),
    '2': chr(31),
    '3': chr(32),
    '4': chr(33),
    '5': chr(34),
    '6': chr(35),
    '7': chr(36),
    '8': chr(37),
    '9': chr(38),
    '0': chr(39),
    ' ': chr(44),
    # Control keys
    'ret': chr(40), #
    'esc': chr(41),
    'del': chr(42), #
    'tab': chr(43), #
    'cap': chr(57), #
    'f1':  chr(58),
    'right_arrow': chr(0x4F),
    'left_arrow':  chr(0x50), #
    'down_arrow':  chr(0x51), #
    'up_arrow':    chr(0x52), #
    NULL_CHAR: NULL_CHAR
}

def send_thread( queue, macros ):
    print(macros)
    while True:
        keys = queue.get()
        print(f'Got {keys}')
        if keys in macros:
            print(f"Handling macro {macros[keys]}")
            handle_macro( macros[keys] )

def handle_macro( steps ):
    for step in steps:
        if step['type'] == 'key':
            for key in step['keys']:
                send_key(key)
            send_key(NULL_CHAR)
        elif step['type'] == 'string':
            for key_list in step['keys']:
                for key in key_list:
                    send_key(key)
                    time.sleep(0.000000001)
            send_key(NULL_CHAR)
        elif step['type'] == 'wait':
            seconds = 0
            if 'seconds' in step:
                seconds = step['seconds']
            time.sleep(seconds)
        # elif step['type'] == 'mouse':
        #     if 'absolute' in step:
        #         absolute = True
        #         x = step['absolute']['x']
        #         y = step['absolute']['y']
        #     else:
        #         absolute = False
        #         x = step['relative']['x']
        #         y = step['relative']['y']
        #     duration = 0
        #     if 'duration' in step:
        #         duration = step['duration']
        #     keyboard.mouse.move( x, y, absolute, duration )

def send_key( key ):
    print(f'sending {key}')
    if key in transform_key:
        report = NULL_CHAR*2 + transform_key[key] + NULL_CHAR*5
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())

if __name__ == '__main__':
    # Parse the yaml and create a dictionary
    document = ''
    with open( MACRO_FILE, 'r' ) as file:
        document = ''.join(file.readlines())

    macros = yaml.safe_load(document)['macros']

    # Setup multiprocessing
    q = mp.Queue()
    p1 = mp.Process(target=send_thread, args=(q, macros,))
    p2 = mp.Process(target=receive_thread, args=(q,))

    p1.start() 
    p2.start() 

    p1.join()
    p2.join()