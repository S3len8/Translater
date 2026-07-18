from pynput import mouse, keyboard
import math
import pyperclip
import time
import requests


x_start = 0
y_start = 0
is_dragging = False
DRAG_THRESHOLD = 12


def translate():
    text_to_translate = pyperclip.paste().strip()
    url = f"https://lingva.ml/api/v1/auto/uk/{text_to_translate}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data.get("translation")
        print(result)
        time.sleep(0.05)


hotkeys = keyboard.GlobalHotKeys({
    '<ctrl>+c': translate,
    '<ctrl>+с': translate,
})


def on_click_mouse(x, y, button, pressed):
    global x_start, y_start, is_dragging
    if button == mouse.Button.left:
        if pressed:
            x_start, y_start = x, y
            is_dragging = True
        else:
            if is_dragging:
                is_dragging = False
                distance = math.sqrt((x - x_start) ** 2 + (y - y_start) ** 2)
                if distance > DRAG_THRESHOLD:
                    print("distance", distance)
                    time.sleep(0.5)


def on_move_mouse(x, y):
    pass


if "__main__" == __name__:
    mouse_ls = mouse.Listener(on_click=on_click_mouse, on_move=on_move_mouse)
    keyboard_ls = hotkeys

    mouse_ls.start()
    keyboard_ls.start()

    mouse_ls.join()
    keyboard_ls.join()