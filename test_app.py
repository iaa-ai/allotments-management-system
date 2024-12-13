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

# Test for POST /departments (success case)
@patch('app.get_db_connection')  
def test_add_department(mock_get_db_connection, test_token):
    mock_conn = MagicMock()  
    mock_cursor = MagicMock() 
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn 

    data = {
        'Managers_Name': 'Jane Doe',
        'Email_Address': 'jane@example.com',
        'Mobile_Cell_Phone_Number': '9876543210'
    }

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'}  
        response = client.post('/departments', json=data, headers=headers)  

    assert response.status_code == 201  
    assert b'Department added successfully' in response.data 

# Test for POST /departments when required fields are missing
def test_add_department_missing_fields(test_token):
    data = {'Managers_Name': 'Jane Doe'}  # Prepare incomplete data for department

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'} 
        response = client.post('/departments', json=data, headers=headers) 

    assert response.status_code == 400  
    assert b'Missing required fields' in response.data  

# Test for POST /departments (failure case - db error)
@patch('app.get_db_connection') 
def test_add_department_db_error(mock_get_db_connection, test_token):
    mock_conn = MagicMock()  
    mock_conn.cursor.side_effect = Exception("Database error")  
    mock_get_db_connection.return_value = mock_conn 

    data = {
        'Managers_Name': 'Jane Doe',
        'Email_Address': 'jane@example.com',
        'Mobile_Cell_Phone_Number': '9876543210'
    }

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'}  
        response = client.post('/departments', json=data, headers=headers)

    assert response.status_code == 500 
    assert b'Database error' in response.data  

# Test for PUT /departments/<id> (success case)
@patch('app.get_db_connection') 
def test_update_department(mock_get_db_connection):
    mock_conn = MagicMock() 
    mock_cursor = MagicMock() 
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor  
    mock_get_db_connection.return_value = mock_conn 

    data = {
        'Managers_Name': 'John Doe',
        'Email_Address': 'john.doe@example.com',
        'Mobile_Cell_Phone_Number': '1122334455'
    }

    with app.test_client() as client:
        response = client.put('/departments/1', json=data)  

    assert response.status_code == 200  
    assert b'Department updated successfully' in response.data  

# Test for PUT /departments/<id> (not found)
@patch('app.get_db_connection')  
def test_update_department_not_found(mock_get_db_connection):
    mock_conn = MagicMock() 
    mock_cursor = MagicMock() 
    mock_cursor.fetchone.return_value = None 
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn 
 
    data = {
        'Managers_Name': 'John Doe',
        'Email_Address': 'john.doe@example.com',
        'Mobile_Cell_Phone_Number': '1122334455'
    }

    with app.test_client() as client:
        response = client.put('/departments/999', json=data)

    assert response.status_code == 404  
    assert b'Department not found' in response.data  

# Test for PUT /departments/<id> (database error)
@patch('app.get_db_connection') 
def test_update_department_db_error(mock_get_db_connection):
    mock_conn = MagicMock() 
    mock_conn.cursor.side_effect = Exception("Database error")  
    mock_get_db_connection.return_value = mock_conn 

    data = {
        'Managers_Name': 'John Doe',
        'Email_Address': 'john.doe@example.com',
        'Mobile_Cell_Phone_Number': '1122334455'
    }

    with app.test_client() as client:
        response = client.put('/departments/1', json=data)  

    assert response.status_code == 500 
    assert b'Database error' in response.data  

# Test for DELETE /departments/<id> (success case)
@patch('app.get_db_connection')  
def test_delete_department(mock_get_db_connection, test_token):
    mock_conn = MagicMock() 
    mock_cursor = MagicMock() 
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor 
    mock_get_db_connection.return_value = mock_conn 

    mock_cursor.fetchone.return_value = {'Department_ID': 1, 'Managers_Name': 'John',
                                         'Email_Address': 'john@example.com', 'Mobile_Cell_Phone_Number': '1234567890'}

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'}  
        response = client.delete('/departments/1', headers=headers)  

    assert response.status_code == 200  
    assert b'Department deleted successfully' in response.data  

# Test for DELETE /departments/<id> (not found)
@patch('app.get_db_connection')
def test_delete_department_not_found(mock_get_db_connection, test_token):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'} 
        response = client.delete('/departments/999', headers=headers)  

    assert response.status_code == 404
    assert b'Department not found' in response.data

# Test for DELETE /departments/<id> (database error)
@patch('app.get_db_connection')
def test_delete_department_db_error(mock_get_db_connection, test_token):
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("Database error")
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        headers = {'Authorization': f'Bearer {test_token}'}  
        response = client.delete('/departments/1', headers=headers)

    assert response.status_code == 500
    assert b'Database error' in response.data

# Test for GET /sites (Fetch all sites)
@patch('app.get_db_connection')
def test_get_sites(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [{'Site_ID': 1, 'Department_ID': 1, 'Managers_Name': 'Alice', 'Mobile_Cell_Phone_Number': '1234567890'}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/sites')

    assert response.status_code == 200
    assert b'Alice' in response.data
    assert b'1234567890' in response.data


# Test for GET /sites/<id> (Fetch a specific site by ID)
@patch('app.get_db_connection')
def test_get_site(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {'Site_ID': 1, 'Department_ID': 1, 'Managers_Name': 'Alice', 'Mobile_Cell_Phone_Number': '1234567890'}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/sites/1')

    assert response.status_code == 200
    assert b'Alice' in response.data
    assert b'1234567890' in response.data


# Test for GET /sites/<id> (Site not found)
@patch('app.get_db_connection')
def test_get_site_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/sites/999')  

    assert response.status_code == 404
    assert b'Site not found' in response.data


# Test for POST /sites (Add a new site)
@patch('app.get_db_connection')
def test_add_site(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Department_ID': 1,
        'Managers_Name': 'Bob',
        'Mobile_Cell_Phone_Number': '9876543210'
    }

    with app.test_client() as client:
        response = client.post('/sites', json=data)

    assert response.status_code == 201
    assert b'Site added successfully' in response.data

# Test for POST /sites (Missing required fields)
def test_add_site_missing_fields():
    data = {'Department_ID': 1}

    with app.test_client() as client:
        response = client.post('/sites', json=data)

    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Test for PUT /sites/<id> (Update site - success case)
@patch('app.get_db_connection')
def test_update_site(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Department_ID': 1,
        'Managers_Name': 'Alice',
        'Mobile_Cell_Phone_Number': '1234567890'
    }

    with app.test_client() as client:
        response = client.put('/sites/1', json=data)

    assert response.status_code == 200
    assert b'Site updated successfully' in response.data


# Test for PUT /sites/<id> (Site not found)
@patch('app.get_db_connection')
def test_update_site_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Department_ID': 1,
        'Managers_Name': 'Alice',
        'Mobile_Cell_Phone_Number': '1234567890'
    }

    with app.test_client() as client:
        response = client.put('/sites/999', json=data)

    assert response.status_code == 404
    assert b'Site not found' in response.data


# Test for DELETE /sites/<id> (Delete site - success case)
@patch('app.get_db_connection')
def test_delete_site(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn
    mock_cursor.fetchone.return_value = {'Site_ID': 1, 'Department_ID': 1, 'Managers_Name': 'Alice', 'Mobile_Cell_Phone_Number': '1234567890'}

    with app.test_client() as client:
        response = client.delete('/sites/1')

    assert response.status_code == 200
    assert b'Site deleted successfully' in response.data

# Test for DELETE /sites/<id> (Site not found)
@patch('app.get_db_connection')
def test_delete_site_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/sites/999')  

    assert response.status_code == 404
    assert b'Site not found' in response.data

# Test for DELETE /sites/<id> (Database error)
@patch('app.get_db_connection')
def test_delete_site_db_error(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("Database error")
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/sites/1')

    assert response.status_code == 500
    assert b'Database error' in response.data

# Test for GET /residents (Fetch all residents)
@patch('app.get_db_connection')
def test_get_residents(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'Resident_ID': 1, 'Resident_Details': 'John Doe', 'Date_First_Registered': '2020-01-01', 'Date_Of_Birth': '1985-01-01'}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/residents')

    assert response.status_code == 200
    assert b'John Doe' in response.data

# Test for GET /residents/<id> (Fetch a specific resident by ID)
@patch('app.get_db_connection')
def test_get_resident(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'Resident_ID': 1, 'Resident_Details': 'John Doe', 'Date_First_Registered': '2020-01-01', 'Date_Of_Birth': '1985-01-01'}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/residents/1')

    assert response.status_code == 200
    assert b'John Doe' in response.data

# Test for GET /residents/<id> (Resident not found)
@patch('app.get_db_connection')
def test_get_resident_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/residents/999')  

    assert response.status_code == 404
    assert b'Resident not found' in response.data


# Test for POST /residents (Add a new resident)
@patch('app.get_db_connection')
def test_add_resident(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Resident_Details': 'Jane Doe',
        'Date_First_Registered': '2023-01-01',
        'Date_Of_Birth': '1990-01-01'
    }

    with app.test_client() as client:
        response = client.post('/residents', json=data)

    assert response.status_code == 201
    assert b'Resident added successfully' in response.data

# Test for POST /residents (Missing required fields)
def test_add_resident_missing_fields():
    data = {'Resident_Details': 'Jane Doe'}

    with app.test_client() as client:
        response = client.post('/residents', json=data)

    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Test for PUT /residents/<id> (Update resident - success case)
@patch('app.get_db_connection')
def test_update_resident(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Resident_Details': 'John Doe Updated',
        'Date_First_Registered': '2020-01-01',
        'Date_Of_Birth': '1985-01-01'
    }

    with app.test_client() as client:
        response = client.put('/residents/1', json=data)

    assert response.status_code == 200
    assert b'Resident updated successfully' in response.data

# Test for PUT /residents/<id> (Resident not found)
@patch('app.get_db_connection')
def test_update_resident_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Resident_Details': 'John Doe Updated',
        'Date_First_Registered': '2020-01-01',
        'Date_Of_Birth': '1985-01-01'
    }

    with app.test_client() as client:
        response = client.put('/residents/999', json=data)

    assert response.status_code == 404
    assert b'Resident not found' in response.data

# Test for DELETE /residents/<id> (Delete resident - success case)
@patch('app.get_db_connection')
def test_delete_resident(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn
    mock_cursor.fetchone.return_value = {'Resident_ID': 1, 'Resident_Details': 'John Doe', 'Date_First_Registered': '2020-01-01', 'Date_Of_Birth': '1985-01-01'}

    with app.test_client() as client:
        response = client.delete('/residents/1')

    assert response.status_code == 200
    assert b'Resident deleted successfully' in response.data

# Test for DELETE /residents/<id> (Resident not found)
@patch('app.get_db_connection')
def test_delete_resident_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/residents/999')  

    assert response.status_code == 404
    assert b'Resident not found' in response.data

# Test for DELETE /residents/<id> (Database error)
@patch('app.get_db_connection')
def test_delete_resident_db_error(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("Database error")
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/residents/1')

    assert response.status_code == 500
    assert b'Database error' in response.data

# Test for GET /rentals (Fetch all rentals)
@patch('app.get_db_connection')
def test_get_rentals(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'Rental_ID': 1, 'Allotment_ID': 1, 'Resident_ID': 1, 'Date_Rented_From': '2022-01-01', 'Date_Rented_To': '2023-01-01'}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/rentals')

    assert response.status_code == 200
    assert b'2022-01-01' in response.data
    assert b'2023-01-01' in response.data

# Test for GET /rentals/<id> (Fetch a specific rental by ID)
@patch('app.get_db_connection')
def test_get_rental(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'Rental_ID': 1, 'Allotment_ID': 1, 'Resident_ID': 1, 'Date_Rented_From': '2022-01-01', 'Date_Rented_To': '2023-01-01'}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/rentals/1')

    assert response.status_code == 200
    assert b'2022-01-01' in response.data
    assert b'2023-01-01' in response.data

# Test for GET /rentals/<id> (Rental not found)
@patch('app.get_db_connection')
def test_get_rental_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/rentals/999')  

    assert response.status_code == 404
    assert b'Rental not found' in response.data

# Test for POST /rentals (Add a new rental)
@patch('app.get_db_connection')
def test_add_rental(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Allotment_ID': 1,
        'Resident_ID': 1,
        'Date_Rented_From': '2022-01-01',
        'Date_Rented_To': '2023-01-01'
    }

    with app.test_client() as client:
        response = client.post('/rentals', json=data)

    assert response.status_code == 201
    assert b'Rental added successfully' in response.data

# Test for POST /rentals (Missing required fields)
def test_add_rental_missing_fields():
    data = {'Allotment_ID': 1, 'Resident_ID': 1}
    with app.test_client() as client:
        response = client.post('/rentals', json=data)

    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Test for PUT /rentals/<id> (Update rental - success case)
@patch('app.get_db_connection')
def test_update_rental(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Allotment_ID': 1,
        'Resident_ID': 1,
        'Date_Rented_From': '2022-01-01',
        'Date_Rented_To': '2023-01-01'
    }

    with app.test_client() as client:
        response = client.put('/rentals/1', json=data)

    assert response.status_code == 200
    assert b'Rental updated successfully' in response.data

# Test for PUT /rentals/<id> (Rental not found)
@patch('app.get_db_connection')
def test_update_rental_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Allotment_ID': 1,
        'Resident_ID': 1,
        'Date_Rented_From': '2022-01-01',
        'Date_Rented_To': '2023-01-01'
    }

    with app.test_client() as client:
        response = client.put('/rentals/999', json=data)

    assert response.status_code == 404
    assert b'Rental not found' in response.data

# Test for DELETE /rentals/<id> (Delete rental - success case)
@patch('app.get_db_connection')
def test_delete_rental(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn
    mock_cursor.fetchone.return_value = {'Rental_ID': 1, 'Allotment_ID': 1, 'Resident_ID': 1, 'Date_Rented_From': '2022-01-01', 'Date_Rented_To': '2023-01-01'}

    with app.test_client() as client:
        response = client.delete('/rentals/1')

    assert response.status_code == 200
    assert b'Rental deleted successfully' in response.data

# Test for DELETE /rentals/<id> (Rental not found)
@patch('app.get_db_connection')
def test_delete_rental_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/rentals/999')  

    assert response.status_code == 404
    assert b'Rental not found' in response.data

# Test for DELETE /rentals/<id> (Database error)
@patch('app.get_db_connection')
def test_delete_rental_db_error(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("Database error")
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/rentals/1')

    assert response.status_code == 500
    assert b'Database error' in response.data

# Test for GET /allotments (Fetch all allotments)
@patch('app.get_db_connection')
def test_get_allotments(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'Allotment_ID': 1, 'Site_ID': 1, 'Allotment_Location': 'North Side', 'Size': 100, 'Annual_Rental': 1200}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/allotments')

    assert response.status_code == 200
    assert b'North Side' in response.data
    assert b'1200' in response.data

# Test for GET /allotments/<id> (Fetch a specific allotment by ID)
@patch('app.get_db_connection')
def test_get_allotment(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'Allotment_ID': 1, 'Site_ID': 1, 'Allotment_Location': 'North Side', 'Size': 100, 'Annual_Rental': 1200}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/allotments/1')

    assert response.status_code == 200
    assert b'North Side' in response.data
    assert b'1200' in response.data


# Test for GET /allotments/<id> (Allotment not found)
@patch('app.get_db_connection')
def test_get_allotment_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.get('/allotments/999')  

    assert response.status_code == 404
    assert b'Allotment not found' in response.data


# Test for POST /allotments (Add a new allotment)
@patch('app.get_db_connection')
def test_add_allotment(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Site_ID': 1,
        'Allotment_Location': 'East Side',
        'Size': 150,
        'Annual_Rental': 1500
    }

    with app.test_client() as client:
        response = client.post('/allotments', json=data)

    assert response.status_code == 201
    assert b'Allotment added successfully' in response.data

# Test for POST /allotments (Missing required fields)
def test_add_allotment_missing_fields():
    data = {'Site_ID': 1, 'Allotment_Location': 'East Side'}
    with app.test_client() as client:
        response = client.post('/allotments', json=data)

    assert response.status_code == 400
    assert b'Missing required fields' in response.data

# Test for PUT /allotments/<id> (Update allotment - success case)
@patch('app.get_db_connection')
def test_update_allotment(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Site_ID': 1,
        'Allotment_Location': 'South Side',
        'Size': 120,
        'Annual_Rental': 1300
    }

    with app.test_client() as client:
        response = client.put('/allotments/1', json=data)

    assert response.status_code == 200
    assert b'Allotment updated successfully' in response.data

# Test for PUT /allotments/<id> (Allotment not found)
@patch('app.get_db_connection')
def test_update_allotment_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    data = {
        'Site_ID': 1,
        'Allotment_Location': 'South Side',
        'Size': 120,
        'Annual_Rental': 1300
    }

    with app.test_client() as client:
        response = client.put('/allotments/999', json=data)

    assert response.status_code == 404
    assert b'Allotment not found' in response.data

# Test for DELETE /allotments/<id> (Delete allotment - success case)
@patch('app.get_db_connection')
def test_delete_allotment(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    mock_cursor.fetchone.return_value = {'Allotment_ID': 1, 'Site_ID': 1, 'Allotment_Location': 'East Side', 'Size': 150, 'Annual_Rental': 1500}

    with app.test_client() as client:
        response = client.delete('/allotments/1')

    assert response.status_code == 200
    assert b'Allotment deleted successfully' in response.data

# Test for DELETE /allotments/<id> (Allotment not found)
@patch('app.get_db_connection')
def test_delete_allotment_not_found(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/allotments/999')  

    assert response.status_code == 404
    assert b'Allotment not found' in response.data

# Test for DELETE /allotments/<id> (Database error)
@patch('app.get_db_connection')
def test_delete_allotment_db_error(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("Database error")
    mock_get_db_connection.return_value = mock_conn

    with app.test_client() as client:
        response = client.delete('/allotments/1')

    assert response.status_code == 500
    assert b'Database error' in response.data
