from src import app as app_module


def test_get_activities(client):
    # Arrange: none
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)
    assert "Chess Club" in resp.json()


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]


def test_signup_already_signed_up_400(client):
    # Arrange
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    assert email in app_module.activities[activity]["participants"]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400


def test_signup_activity_not_found_404(client):
    # Arrange
    activity = "NonExistent"
    email = "x@mergington.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "temp@mergington.edu"
    if email not in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].append(email)
    assert email in app_module.activities[activity]["participants"]
    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_remove_participant_not_found_404(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]
    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert resp.status_code == 404


def test_remove_activity_not_found_404(client):
    # Arrange
    activity = "NoActivity"
    email = "x@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert resp.status_code == 404
