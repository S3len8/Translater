import asyncio
import math
import time
import pyperclip
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from desktop.client import send_to_endpoint1, handle_endpoint1_result 

x_start = 0
y_start = 0
is_dragging = False
DRAG_THRESHOLD = 12
keyboard_controller = keyboard.Controller()
is_pressed_ctrl = False
keyboard_ls = None
mouse_ls = None

def on_key_press(key):
    global is_pressed_ctrl
    if key in (Key.ctrl_l, Key.ctrl_r):
        is_pressed_ctrl = True

def on_key_release(key):
    global is_pressed_ctrl
    if key in (Key.ctrl_l, Key.ctrl_r):
        is_pressed_ctrl = False

def on_click_mouse(x, y, button, pressed, loop):
    global x_start, y_start, is_dragging

    if button != mouse.Button.left:
        return

    if pressed:
        x_start, y_start = x, y
        is_dragging = True
        return

    if not is_dragging:
        return

    is_dragging = False
    distance = math.sqrt((x - x_start) ** 2 + (y - y_start) ** 2)

    if distance <= DRAG_THRESHOLD:
        return

    print("distance", distance)
    time.sleep(0.12)

    keyboard_controller.press(Key.ctrl_l)
    keyboard_controller.press(KeyCode.from_vk(67))
    keyboard_controller.release(KeyCode.from_vk(67))
    keyboard_controller.release(Key.ctrl_l)

    selected_text = ""
    for _ in range(10):
        time.sleep(0.03)
        selected_text = pyperclip.paste().strip()
        if selected_text:
            break

    if not selected_text:
        print("Не вдалося отримати виділений текст")
        return

    future = asyncio.run_coroutine_threadsafe(
        send_to_endpoint1(selected_text),
        loop,
    )
    future.add_done_callback(handle_endpoint1_result)

def on_move_mouse(x, y):
    pass

def start_listening(loop):
    global keyboard_ls, mouse_ls

    keyboard_ls = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release,
    )
    mouse_ls = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_click_mouse(
            x,
            y,
            button,
            pressed,
            loop,
        ),
        on_move=on_move_mouse,
    )

    keyboard_ls.start()
    mouse_ls.start()

def stop_listening():
    global keyboard_ls, mouse_ls

    if keyboard_ls:
        keyboard_ls.stop()
        keyboard_ls = None

    if mouse_ls:
        mouse_ls.stop()
        mouse_ls = None
