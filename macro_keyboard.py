import sys
import yaml
import keyboard
import time

MACRO_FILE = "macros.yaml"

def handle_macro( steps ):
    for step in steps:
        if step['type'] == 'Key':
            for key in step['keys']:
                keyboard.send(key)
        elif step['type'] == 'String':
            for key in step['keys']:
                keyboard.write(key)
        elif step['type'] == 'Wait':
            time.sleep(step['keys'])

if __name__ == '__main__':
    # Parse the yaml and create a dictionary
    document = ''
    with open( MACRO_FILE, 'r' ) as file:
        document = ''.join(file.readlines())

    macros = yaml.safe_load(document)['macros']

    print(macros)
    for key, steps in macros.items():
        keyboard.add_hotkey(key, handle_macro, args=[steps])

    # TODO: Probably don't want this in the final port
    # Exit
    keyboard.wait('esc')
    print("Exiting")
    keyboard.unhook_all()
    keyboard.unhook_all_hotkeys()