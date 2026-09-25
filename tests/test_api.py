from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    activities.clear()
    activities.update(deepcopy(original))
    yield
    activities.clear()
    activities.update(deepcopy(original))


def test_duplicate_registration_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_adds_participant():
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_unregister_participant_removes_email():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity}/participants?email={email}")

    assert delete_response.status_code == 200
    assert email not in activities[activity]["participants"]
