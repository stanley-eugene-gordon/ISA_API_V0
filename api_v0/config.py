import os
from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import openai
from typing import Union


load_dotenv()
openai.api_key = os.getenv("openai_key")

class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_port: Union[int, str]
    database_name: str
    db_pool_size = 83
    web_concurrency = 3
    pool_size = db_pool_size // web_concurrency


    # FastAPI
    host: str = "0.0.0.0"
    port: int = 5000

    # OpenAI key
    openai_key: str 

 
@lru_cache()
def get_settings() -> Settings:
    return Settings()

    