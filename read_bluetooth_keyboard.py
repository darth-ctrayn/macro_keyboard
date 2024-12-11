import keyboard

def hotkey_callback( queue, key ):
    queue.put(key)

def recieve_keyboard_thread( queue, macros ):
    for key in macros:
        if key.isalnum():
            keyboard.add_hotkey(key.lower(), hotkey_callback, (queue, key,) )

    keyboard.wait()