from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = "5432"
    postgres_username: str = "postgres"
    postgres_password: str
    postgres_db: str = "weather"
    redis_host: str = "localhost"
    redis_port: int = "6379"
    weather_api_key: str
    weather_url: str = "https://api.openweathermap.org/data/2.5"
    current_weather_cache_ttl: int = 600
    forecast_cache_ttl: int = 3600
    rate_limit_count: int = 60
    rate_limit_window: int = 60


class MailSettings(BaseSettings):
    mail_host: str
    mail_port: int
    mail_username: str
    mail_password: str


base_settings = Settings()
mail_settings = MailSettings()
