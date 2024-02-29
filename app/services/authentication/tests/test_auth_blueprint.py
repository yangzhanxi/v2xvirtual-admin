import pytest


@pytest.mark.skip
def test_auth(client):
    # Test login without username
    response = client.post("/api/login")
    assert {"msg": "Invalid username or password."} == response.json
    assert 422 == response.status_code

    # Test login without password
    response = client.post(
        "/api/login",
        json={
            "username": "admin"
        })
    assert {"msg": "Invalid username or password."} == response.json
    assert 422 == response.status_code

    # Test login with invalid username and password
    response = client.post(
        "/api/login",
        json={
            "username": "",
            "password": ""
        })
    assert {"msg": "Invalid username or password."} == response.json
    assert 422 == response.status_code

    # Test login successfully
    response = client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "password"
        })
    assert "Login successfully." == response.json["msg"]
    assert "admin" == response.json["username"]
    assert "access_toke" in response.json.keys()
    assert 200 == response.status_code
    access_token = response.json["access_toke"]

    # Test user is already logged in
    response = client.post(
        "/api/login",
        json={
            "username": "admin",
            "password": "password"
        })
    assert "User is already logged in." == response.json["msg"]
    assert 200 == response.status_code

    # Test logout
    response = client.post(
        "/api/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        })
    assert "Logged out successfully." == response.json["msg"]
    assert 200 == response.status_code
