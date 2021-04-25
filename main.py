import pyautogui
import win32clipboard
from KoreanToEnglish import KorTransform2Eng
from WordEngine import WordEngine
from KeyboardInput import oneKeyInput


def typeWord(mode: str) -> str:
    ATK_MODE = '1'
    LONG_MODE = '2'

    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    pyautogui.press("backspace")
    pyautogui.press("backspace")

    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    frontChar = data[0]

    if mode == ATK_MODE:
        word = wordEngine.getWord('atk', frontChar)
    elif mode == LONG_MODE:
        word = wordEngine.getWord('long', frontChar)

    if word:
        pyautogui.typewrite(KorTransform2Eng(word))
        pyautogui.press("enter")

if __name__ == '__main__':
    wordEngine = WordEngine()

    while True:
        try:
            key = oneKeyInput()
        except:
            continue

        if key == '0':
            print('End KKuTu Script!')
            break

        elif key == '1' or key == '2':
            typeWord(key)
                
        elif key == '9':
            wordEngine.reset()