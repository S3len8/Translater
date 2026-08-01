from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from core.config import Settings
from routers import translate, export
from core.listeners import start_listening, stop_listening
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    start_listening(loop)
    print("🚀 Слухачі мишки та клавіатури успішно запущені!")

    yield

    stop_listening()
    print("🛑 Слухачі зупинені.")


app = FastAPI(
    title="Translation App API",
    lifespan=lifespan
)
settings = Settings()
app.include_router(translate.router)
app.include_router(export.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
