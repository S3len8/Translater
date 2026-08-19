import httpx
from backend.schemas.translate import TranslationResult

class Translate:
    def __init__(self):
        pass

    async def translate(self, word):
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "uk",
            "dt": "t",
            "q": word,
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
                    payload = TranslationResult(
                        word=word,
                        translation=result,
                        transcription=None,
                    )
                    return payload
