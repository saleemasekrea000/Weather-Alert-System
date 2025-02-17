import asyncio
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.celery_app import app
from src.database import SessionLocal
from src.mailingsys.mailer import send_mail
from src.models.alert import Alert
from src.models.subscription import Subscription
from src.models.weather import Weather
from src.settings import base_settings
from src.utils.weather import send_request, store_weather_data


@app.task(name="send_subscription_email")
def send_subscription_email(user_email: str, city: str):
    subject = "Welcome to our Weather Alert System!"
    body = f"Thank you for subscribing to Weather Alerts! You will now receive weather alerts for {city} "
    send_mail(user_email, subject, body)
    return "Email sent successfully!"


@app.task(name="send_weather_alert_email")
def send_weather_alert_email(user_email: str, city: str, condition_triggered: dict):
    """
    Sends a weather alert email to the user if their conditions are met.
    """
    subject = f"⚠ Weather Alert for {city}!"
    body = (
        f"Dear User,\n\n"
        f"The weather condition in {city} has met your alert criteria.\n\n"
        f"📌 Current Condition:\n"
        f"- Temperature: {condition_triggered.get('temperature', 'N/A')}°C\n"
        f"- Threshold Set: {condition_triggered.get('threshold', 'N/A')}°C\n\n"
        f"Stay safe and check the latest updates!\n\n"
        f"Best regards,\n"
        f"Weather Alert System"
    )

    send_mail(user_email, subject, body)
    return f"Alert email sent to {user_email} for {city}"


@app.task(name="update_weather_data")
def update_weather_data(city: str):
    """
    Updates weather data for a given city and checks if any alert conditions are triggered.
    """
    url = f"{base_settings.weather_url}/weather"

    params = {
        "q": city,
        "appid": base_settings.weather_api_key,
    }
    # here i create a mini loop event to be able to wait for the response
    # as celery task is sync ...
    weather_data = asyncio.run(send_request(url, params))
    with SessionLocal() as db:
        store_weather_data(db, weather_data)
        check_and_trigger_alerts(db)
    print(f"Updated weather data for {city}")


@app.task(name="update_all_weather_data")
def update_all_weather_data():
    """
    Updates weather data for all subscribed cities.
    """
    with SessionLocal() as db:
        cities = db.query(Subscription.city).all()
        # cities will be a list of tuples, so extract city names
        city_list = [city[0] for city in cities]
    for city in city_list:
        update_weather_data.delay(city)
    return f"Triggered updates for {len(city_list)} cities."


def check_and_trigger_alerts(db: Session) -> None:
    """
    Check all active subscriptions and compare their thresholds against
    the latest weather data. If a threshold is exceeded, create an alert
    and send a notification email.
    """
    subscriptions = db.query(Subscription).all()

    for sub in subscriptions:
        sub_city = sub.city.lower()
        # Get the latest weather data for the subscriber's city
        weather = db.query(Weather).filter(Weather.city == sub_city).first()
        if not weather:
            raise HTTPException(
                status_code=404, detail=f"No weather data found for city: {sub.city}"
            )

        # Check if the weather condition exceeds the subscriber's threshold
        if weather.temperature >= sub.condition_thresholds["temperature"]:
            # Check if an active alert already exists for this subscription
            existing_alert = (
                db.query(Alert)
                .filter(Alert.subscription_id == sub.id, Alert.is_active == True)
                .first()
            )
            if not existing_alert:
                # Create a new alert
                alert = Alert(
                    subscription_id=sub.id,
                    condition_triggered={
                        "temperature": weather.temperature,
                        "threshold": sub.condition_thresholds["temperature"],
                    },
                    is_active=True,
                    triggered_at=datetime.now(timezone.utc),
                )
                db.add(alert)
                db.commit()
                db.refresh(alert)

                # Send notification asynchronously
                send_weather_alert_email.delay(
                    sub.email, sub.city, alert.condition_triggered
                )
