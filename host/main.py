import keyboard, time, subprocess, yaml

MACRO_FILE='macros.yml'

def handle_macro( steps ):
    print(f"Handling macro with steps {steps}")
    for step in steps:
        if step['type'] == 'keys':
            for keys in step['keys']:
                parse_and_send(keys)
        elif step['type'] == 'wait':
            seconds = 0
            if 'seconds' in step:
                seconds = step['seconds']
            time.sleep(seconds)
        elif step['type'] == 'system':
            for command in step['keys']:
                proc = subprocess.run(command.split(' '), capture_output=True)
                if 'output' in step and step['output'] == 'True':
                    output = proc.stdout.decode()
                    output = output.replace('{', '<')
                    output = output.replace('}', '>')
                    output = output.replace('\n', '{ret}')
                    parse_and_send( output )

def parse_and_send( keys:str ):
    to_send = parse( keys )
    for keys in to_send:
        keyboard.press_and_release(keys)

def parse( keys:str ):
    """Takes 'keys' as a input string, anything in brackets {} is sent as a single key press (formatted as shift + r, etc...)"""
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

if __name__ == '__main__':
    document = ''
    with open( MACRO_FILE, 'r' ) as file:
        document = ''.join(file.readlines())

    macros = yaml.safe_load(document)['macros']

    print(macros)

    for key, macro in macros.items():
        keyboard.add_hotkey(key, handle_macro, args=(macro,))

    keyboard.wait('ctrl + win + alt + esc')