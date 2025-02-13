from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = "5432"
    postgres_username: str = "postgres"
    postgres_password: str
    postgres_db: str = "weather"
    weather_api_key: str
    weather_url: str = "https://api.openweathermap.org/data/2.5"


base_settings = Settings()
