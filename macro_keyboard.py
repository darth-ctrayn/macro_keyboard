import sys
import yaml
import keyboard

MACRO_FILE = "macros.yaml"

key_shifts = {
    "' '": 'SPACE'
}

if __name__ == '__main__':
    # Parse the yaml and create a dictionary
    document = ''
    with open( MACRO_FILE, 'r' ) as file:
        document = ''.join(file.readlines())

    macros = yaml.safe_load(document)['macros']

    print(macros)
    for key, values in macros.items():
        values = values.lstrip()
        keyboard.add_hotkey(key, keyboard.send, args=[values])

    # TODO: Probably don't want this in the final port
    # Exit
    keyboard.wait('esc')
    print("Exiting")
    keyboard.unhook_all()
    keyboard.unhook_all_hotkeys()