import importlib
from fastapi.testclient import TestClient

import src.app as app_module


def make_client():
    # reload module to reset in-memory activities between tests
    importlib.reload(app_module)
    return TestClient(app_module.app)


def test_get_activities():
    client = make_client()
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity from the initial dataset
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate():
    client = make_client()
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # signup should succeed first time
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # activity should now include the email
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_unregister_flow():
    client = make_client()
    activity = "Basketball Club"
    email = "to_remove@example.com"

    # ensure user is registered
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
import importlib
from fastapi.testclient import TestClient

import src.app as app_module


def make_client():
    # reload module to reset in-memory activities between tests
    importlib.reload(app_module)
    return TestClient(app_module.app)


def test_get_activities():
    client = make_client()
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity from the initial dataset
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate():
    client = make_client()
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # signup should succeed first time
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # activity should now include the email
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_unregister_flow():
    client = make_client()
    activity = "Basketball Club"
    email = "to_remove@example.com"

    # ensure user is registered
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # unregister
    r2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r2.status_code == 200
    assert "Unregistered" in r2.json().get("message", "")

    # email should be gone
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

    # unregister again should return 400
    r3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r3.status_code == 400
