from fastapi import FastAPI

from src.routers import weather

app = FastAPI()

app.include_router(weather.weather_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
