import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def setup_function():
    # Reset the in-memory database before each test
    for activity in activities.values():
        if isinstance(activity["participants"], list):
            activity["participants"].clear()


def test_get_activities():
    # Arrange
    # (Banco já está limpo pelo setup_function)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    assert email not in activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_activity_not_found():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered():
    # Arrange
    email = "already@mergington.edu"
    activity = "Chess Club"
    activities[activity]["participants"].append(email)

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
