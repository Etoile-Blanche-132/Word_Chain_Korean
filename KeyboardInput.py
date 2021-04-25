from pynput import keyboard

def oneKeyInput():
    keyInput = ''

    def onPress(key):
        nonlocal keyInput

        keyInput = key

        return False

    def onRelease(key):
        return False
    
    # Collect events until released
    with keyboard.Listener(
            on_press = onPress,
            on_release = onRelease) as listener:
        listener.join()

    return keyInput.char

if __name__ == "__main__":
    def onPress(key):
        try:
            print('alphanumeric key {0} pressed'.format(key))
        except AttributeError:
            print('special key {0} pressed'.format(key))
    
    def onRelease(key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False
    
    # Collect events until released
    with keyboard.Listener(
            on_press = onPress,
            on_release = onRelease) as listener:
        listener.join()
