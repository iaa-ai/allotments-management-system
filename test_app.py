import pytest
from flask import Flask, jsonify, request
from app import create_jwt, app 
from unittest.mock import patch, MagicMock

# Fixture to generate JWT token
@pytest.fixture
def test_token():
    return create_jwt(user_id="test_user", role="admin")  # Replace with your test user details

# Fixture to set up a test client for Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True  
    with app.test_client() as client:  
        yield client  

# Test case to check if the /departments route returns 401 when no token is provided
def test_get_departments_no_token(client):
    response = client.get('/departments')  
    assert response.status_code == 401  
    assert b'Authorization token is missing' in response.data 

# Test case to check if the /departments route returns 401 with an invalid token
def test_get_departments_invalid_token(client):
    headers = {'Authorization': 'Bearer invalid_token'}  
    response = client.get('/departments', headers=headers)  
    assert response.status_code == 401  
    assert b'Invalid token' in response.data 

# Test for GET /departments endpoint
@patch('app.get_db_connection')  # Mocking the get_db_connection
def test_get_departments(mock_get_db_connection, test_token):
    mock_conn = MagicMock()  
    mock_cursor = MagicMock()  

    # Set up the mock cursor to return fake data for departments
    mock_cursor.fetchall.return_value = [
        {'Department_ID': 1, 'Managers_Name': 'John', 'Email_Address': 'john@example.com',
         'Mobile_Cell_Phone_Number': '1234567890'}
    ]
    
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    # Sending a GET request to the /departments endpoint with the Authorization header containing the test token
    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'}  
        response = client.get('/departments', headers=headers)

    assert response.status_code == 200  
    assert b'John' in response.data 
    assert b'john@example.com' in response.data  

# Test for GET /departments/<id> to fetch a specific department by ID
@patch('app.get_db_connection')  
def test_get_department(mock_get_db_connection):
    mock_conn = MagicMock()  
    mock_cursor = MagicMock()  

    mock_cursor.fetchone.return_value = {'Department_ID': 1, 'Managers_Name': 'John',
                                         'Email_Address': 'john@example.com', 'Mobile_Cell_Phone_Number': '1234567890'}

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/departments/1', headers={'Authorization': f'Bearer {test_token}'})

    assert response.status_code == 200
    assert b'John' in response.data 
    assert b'john@example.com' in response.data  

# Test for GET /departments/<id> when department is not found
@patch('app.get_db_connection') 
def test_get_department_not_found(mock_get_db_connection):
    mock_conn = MagicMock() 
    mock_cursor = MagicMock() 

    mock_cursor.fetchone.return_value = None  
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn  

    with app.test_client() as client:
        response = client.get('/departments/999')  

    assert response.status_code == 404 
    assert b'Department not found' in response.data 
