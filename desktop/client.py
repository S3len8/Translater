import httpx
from desktop.config import ENDPOINT_URL

async def send_to_endpoint1(word: str) -> dict:
    async with httpx.AsyncClient(
        base_url=ENDPOINT_URL,
    ) as client:
        response = await client.post("/translate", json={"word": word})
        response.raise_for_status()
        if response.is_error:
            print(response.text)

        return response.json()


def handle_endpoint1_result(future):
    try:
        result = future.result()
    except Exception as error:
        print(f"Помилка передачі слова на Endpoint 1: {error}")
    else:
        print(f"Endpoint 1 отримав слово: {result}")