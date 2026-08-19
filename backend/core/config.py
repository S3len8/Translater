from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    HOST: str
    PORT: int



    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"),
                                      env_file_encoding="utf-8",
                                      extra="ignore")


settings = Settings()