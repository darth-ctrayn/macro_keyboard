import yaml
import time
import multiprocessing as mp
from read_keypad import *
import os
# from macros_verify import *

MACRO_FILE = "macros.yaml"
NULL_CHAR = chr(0)

transform_key = {
    # String keys
    'a': chr(0x04),
    'b': chr(0x05),
    'c': chr(0x06),
    'd': chr(0x07),
    'e': chr(0x08),
    'f': chr(0x09),
    'g': chr(0x0A),
    'h': chr(0x0B),
    'i': chr(0X0C),
    'j': chr(0x0D),
    'k': chr(0x0E),
    'l': chr(0x0F),
    'm': chr(0x10),
    'n': chr(0x11),
    'o': chr(0x12),
    'p': chr(0x13),
    'q': chr(0x14),
    'r': chr(0x15),
    's': chr(0x16),
    't': chr(0x17),
    'u': chr(0x18),
    'v': chr(0x19),
    'w': chr(0x1A),
    'x': chr(0x1B),
    'y': chr(0x1C),
    'z': chr(0x1D),
    '1': chr(0x1E),
    '2': chr(0x1F),
    '3': chr(0x20),
    '4': chr(0x21),
    '5': chr(0x22),
    '6': chr(0x23),
    '7': chr(0x24),
    '8': chr(0x25),
    '9': chr(0x26),
    '0': chr(0x27),
    'ret': chr(0x28), # Return/Enter
    'esc': chr(0x29),
    'bsp': chr(0x2A), # Backspace
    'tab': chr(0x2B),
    ' ': chr(0x2C),
    '-': chr(0x2D),
    '=': chr(0x2E),
    '[': chr(0x2F),
    ']': chr(0x30),
    '\\': chr(0x31),
    '#': chr(0x32),
    ';': chr(0x33),
    "'": chr(0x34),
    "`": chr(0x35),
    ',': chr(0x36),
    '.': chr(0x37),
    '/': chr(0x38),
    'caps': chr(0x39), # Caps lock
    'f1':  chr(0x3A),
    'f2':  chr(0x3B),
    'f3':  chr(0x3C),
    'f4':  chr(0x3D),
    'f5':  chr(0x3E),
    'f6':  chr(0x3F),
    'f7':  chr(0x40),
    'f8':  chr(0x41),
    'f9':  chr(0x42),
    'f10': chr(0x43),
    'f11': chr(0x44),
    'f12': chr(0x45),
    'pntscn': chr(0x46), # Print screen
    'scllck': chr(0x47), # Scroll lock
    'pause':  chr(0x48),
    'insert': chr(0x49),
    'home':   chr(0x4A),
    'pgup':   chr(0x4B), # Page Up
    'del':    chr(0x4C),
    'end':    chr(0x4D),
    'pgdn':   chr(0x4E),
    'right_arrow': chr(0x4F),
    'left_arrow':  chr(0x50),
    'down_arrow':  chr(0x51),
    'up_arrow':    chr(0x52),
    'nmlck': chr(0x53), # Num Lock
    'null': NULL_CHAR,
    NULL_CHAR: NULL_CHAR
}

def send_thread( queue, macros ):
    print(macros)
    while True:
        keys = queue.get()
        if keys in macros:
            print(f"Handling macro {macros[keys]}")
            handle_macro( macros[keys] )

def handle_macro( steps ):
    for step in steps:
        if step['type'] == 'keys':
            for keys in step['keys']:
                parse_and_send(keys)
        elif step['type'] == 'wait':
            parse_and_send('{null}')
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
    send_key(NULL_CHAR)

def parse_and_send( keys:str ):
    to_send = parse( keys )
    send_array( to_send )

def parse( keys:str ):
    """Takes 'keys' as a input string, anything in brackets {} is a command key (ctl, shift, etc...). To turn off a command key, use {/command} ({/shift}, {/ctl}) returns as array"""
    to_send = []
    current_keys = keys
    while len(current_keys) > 0:
        # Get the first key of the string
        key = current_keys[0]
        current_keys = current_keys.replace(current_keys[0], "", 1)

        # Control keys
        if key == '{':
            to_send.append( current_keys[:current_keys.find('}')])
            current_keys = current_keys[current_keys.find('}') + 1:]
        # Non-control keys (regular keys)
        else:
            to_send.append(key)
    return to_send

def send_array( keys ):
    """Send the array of keys one at a time, with modifiers"""
    valid_modifiers = [
        'rmeta',
        'ralt',
        'rshift',
        'rctl',
        'lmeta',
        'lalt',
        'lshift',
        'lctl',
    ]
    modifier = ['0'] * 8
    for key in keys:
        # Ignore blanks
        if key == '':
            continue

        if key in valid_modifiers:
            modifier[valid_modifiers.index(key)] = '1'
            key = NULL_CHAR
        elif key[0] == '/' and key[1:] in valid_modifiers:
            modifier[valid_modifiers.index(key[1:])] = '0'
            key = NULL_CHAR
        elif ('l' + key) in valid_modifiers:
            modifier[valid_modifiers.index('l' + key)] = '1'
            key = NULL_CHAR
        elif key[0] == '/' and ('l' + key[1:]) in valid_modifiers:
            modifier[valid_modifiers.index("l" + key[1:])] = '0'
            key = NULL_CHAR

        # Send the key
        send_key( key, modifier=int(''.join(modifier), 2) )
        time.sleep(0.000000001)

def send_key( key, modifier=0x0 ):
    print(f'sending {key}')
    if key in transform_key:
        # report = NULL_CHAR*2 + transform_key[key] + NULL_CHAR*5
        report = chr(modifier) + NULL_CHAR + transform_key[key] + NULL_CHAR*5
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())

if __name__ == '__main__':
    # Make sure I'm running alone
    pid = str(os.getpid())
    pidfile = '/tmp/mydaemon.pid'
    if os.path.isfile(pidfile):
        print(f"File {pidfile} already exists, exiting")
        exit(1)
    with open(pidfile, 'w') as file:
        file.write(pid)
    try:
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
    finally:
        os.unlink(pidfile)