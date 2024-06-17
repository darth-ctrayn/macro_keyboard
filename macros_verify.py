LOGGING = True

def log( msg ):
    if LOGGING == True:
        print( msg )

def verify( macros:dict ):
    for key, macro in macros.items():
        log(f'Checking key: {key}')
        if not isinstance( macro, list ):
            raise SyntaxError(f"Datatype for {key} must be a list")
            continue
        for idx in range(len(macro)):
            step = macro[idx]
            if 'type' not in step:
                raise SyntaxError(f"In {key}, list number {idx} must include 'type'")
                continue
            elif step['type'] == 'key':
            elif step['type'] == 'string':
            elif step['type'] == 'wait':
            elif step['type'] == 'mouse':
            else:
                raise SyntaxError(f"In {key}, step {idx} type not recognized: {step['type']}")