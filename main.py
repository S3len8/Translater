from pynput import mouse, keyboard
import math
import pyperclip
import time
import httpx
from core.postgre import get_db
from repositories.history import HistoryRepository
import asyncio


x_start = 0
y_start = 0
is_dragging = False
DRAG_THRESHOLD = 12
keyboard_controller = keyboard.Controller()


async def add_database(word: str, translation: str, transcription: str | None = None):
    async for db in get_db():
        repo = HistoryRepository(db)
        await repo.create_history(word=word, translation=translation, transcription=transcription)


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
                    keyboard_controller.press('c')
                    keyboard_controller.release('c')
                    keyboard_controller.release(keyboard.Key.ctrl_l)
                    for _ in range(10):
                        time.sleep(0.03)
                        if pyperclip.paste() != text:
                            break

                    asyncio.run_coroutine_threadsafe(translate(), loop)


async def translate():
    text_to_translate = pyperclip.paste().strip()
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": "uk",
        "dt": "t",
        "q": text_to_translate,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(url=url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            result = "".join([part[0] for part in data[0] if part[0]])
            print(result)
            if result:
                await add_database(word=text_to_translate, translation=result, transcription=None)


def on_move_mouse(x, y):
    pass


async def main():
    loop = asyncio.get_running_loop()

    mouse_ls = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_click_mouse(x, y, button, pressed, loop),
        on_move=on_move_mouse
    )
    mouse_ls.start()

    while True:
        await asyncio.sleep(3600)

if "__main__" == __name__:
    asyncio.run(main())