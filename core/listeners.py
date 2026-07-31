import asyncio
import math
import time
import pyperclip
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from clients.translate import Translate
from services.translate import TranslateService
from repositories.history import HistoryRepository
from core.postgre import get_db


async def handle_translation_event():
    # 1. Відкриваємо сесію БД
    async for db in get_db():
        # 2. Створюємо Репозиторій з сесією
        history_repo = HistoryRepository(db)

        # 3. Створюємо Сервіс з репозиторієм
        translate_service = TranslateService(history_repo=history_repo)

        # 4. Передаємо Сервіс у Клієнт
        translator = Translate(service=translate_service)

        # 5. Запускаємо переклад
        await translator.translate()
        break

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
    if key in(Key.ctrl_l, Key.ctrl_r):
        is_pressed_ctrl = True

def on_key_release(key):
    global is_pressed_ctrl
    if key in(Key.ctrl_l, Key.ctrl_r):
        is_pressed_ctrl = False


def on_click_mouse(x, y, button, pressed, loop):
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
                    keyboard_controller.press(KeyCode.from_vk(67))
                    keyboard_controller.release(KeyCode.from_vk(67))
                    keyboard_controller.release(keyboard.Key.ctrl_l)
                    for _ in range(10):
                        time.sleep(0.03)
                        if pyperclip.paste() != text:
                            break

                    asyncio.run_coroutine_threadsafe(handle_translation_event(), loop) 



def on_move_mouse(x, y):
    pass


def start_listening(loop):
    global keyboard_ls, mouse_ls
    keyboard_ls = keyboard.Listener(on_press=on_key_press,
                                    on_release=on_key_release
                                    )
    mouse_ls = mouse.Listener(on_click=lambda x, y, button, pressed: on_click_mouse(x, y, button, pressed, loop),
                              on_move=on_move_mouse
                              )

    keyboard_ls.start()
    mouse_ls.start()

def stop_listening():
    global keyboard_ls, mouse_ls

    if keyboard_ls:
        keyboard_ls.stop()
    if mouse_ls:
        mouse_ls.stop()