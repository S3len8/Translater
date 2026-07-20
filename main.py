from pynput import mouse, keyboard
import math
import pyperclip
import time
import requests
import threading


x_start = 0
y_start = 0
is_dragging = False
DRAG_THRESHOLD = 12
keyboard_controller = keyboard.Controller()


def add_database():
    pass 

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
                    text = pyperclip.paste().strip()
                    time.sleep(0.12)
                    keyboard_controller.press(keyboard.Key.ctrl_l)
                    keyboard_controller.press('c')
                    keyboard_controller.release('c')
                    keyboard_controller.release(keyboard.Key.ctrl_l)
                    for _ in range(10):
                        time.sleep(0.03)
                        if pyperclip.paste() != text:
                            break

                    threading.Thread(target=translate, daemon=True).start()


def translate():
    text_to_translate = pyperclip.paste().strip()
    url = f"https://lingva.ml/api/v1/auto/uk/{text_to_translate}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data.get("translation")
        print(result)


def on_move_mouse(x, y):
    pass


if "__main__" == __name__:
    mouse_ls = mouse.Listener(on_click=on_click_mouse, on_move=on_move_mouse)

    mouse_ls.start()

    mouse_ls.join() 