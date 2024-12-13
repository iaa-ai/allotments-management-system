import pytest
from flask import Flask, jsonify, request

from app import create_jwt, app  # Import your app and create_jwt function

# Fixture to generate JWT token
@pytest.fixture
def test_token():
    # Generate a test JWT token with a user_id and role
    return create_jwt(user_id="test_user", role="admin")  # Replace with your test user details

# Fixture to set up a test client for Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode for Flask
    with app.test_client() as client:  # Create a test client to simulate HTTP requests
        yield client  # Return the test client for use in the tests

# Test case to check if the /departments route returns 401 when no token is provided
def test_get_departments_no_token(client):
    response = client.get('/departments')  # Make a GET request to /departments without a token
    assert response.status_code == 401  # Assert that the response status is 401 Unauthorized
    assert b'Authorization token is missing' in response.data  # Assert that the error message is present

# Test case to check if the /departments route returns 401 with an invalid token
def test_get_departments_invalid_token(client):
    headers = {'Authorization': 'Bearer invalid_token'}  # Set an invalid token in the Authorization header
    response = client.get('/departments', headers=headers)  # Make a GET request with the invalid token
    assert response.status_code == 401  # Assert that the response status is 401 Unauthorized
    assert b'Invalid token' in response.data  # Assert that the error message for an invalid token is returned
