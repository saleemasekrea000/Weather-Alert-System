from unittest.mock import patch


def test_subscribe(client, subscription_data):

    with patch("src.services.alert.user_subscribe", return_value=subscription_data):
        response = client.post("/alert/subscribe", json=subscription_data)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["email"] == subscription_data["email"]


def test_active_alerts(client):

    with patch("src.services.alert.get_active_alerts", return_value=[]):
        response = client.get("/alert/active")

        assert response.status_code == 200
