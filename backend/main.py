from fastapi import FastAPI
import uvicorn
from backend.core.config import Settings
from backend.routers import translate, export
from backend.routers import history

app = FastAPI(
    title="Translation App API",
)

settings = Settings()
app.include_router(translate.router)
app.include_router(export.router)
app.include_router(history.router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
