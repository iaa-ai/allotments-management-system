from flask import Flask, jsonify, request
import pymysql
import jwt
import datetime 
from functools import wraps

# ------------------------------------- Security ----------------------------------
# Secret key used to sign and verify JWT tokens
SECRET_KEY = 'bakanese'  # Replace with a strong, unique secret key in production

# Function to create a JWT token
def create_jwt(user_id, role):
    payload = {
        'user_id': user_id,  # User's unique ID
        'role': role,  # User's role
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # Encode the payload using HS256 algorithm

# Function to decode and verify a JWT token
def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

# Decorator to protect routes with optional role-based access control
def jwt_required(role=None):
    def decorator(func):
        @wraps(func)  # Preserve metadata of the original function
        def wrapper(*args, **kwargs):
            # Get the Authorization token from request headers
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'error': 'Authorization token is missing'}), 401

            try:
                # Extract the token part from the "Bearer <token>" format
                token = token.split(" ")[1]

                # Decode and verify the JWT token
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

                # Check for role-based access control (if a role is provided)
                if role and decoded_token['role'] != role:
                    return jsonify({'error': 'Access denied for this role'}), 403

                # Attach the decoded token data to the request object for further use
                request.user = decoded_token
                # Call the original function if the token is valid
                return func(*args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                # Handle the case where the token has expired
                return jsonify({'error': 'Token expired'}), 401
            
            except jwt.InvalidTokenError:

                # Handle the case where the token is invalid
                return jsonify({'error': 'Invalid token'}), 401
        return wrapper
    return decorator


app = Flask(__name__)

# Function to establish a connection to the MySQL database
def get_db_connection():
    return pymysql.connect(
        host='localhost',  # MySQL host (localhost for local development)
        user='root',  # Database username
        password='bakanese',  # Database password
        database='allotments',  # Database name
        cursorclass=pymysql.cursors.DictCursor  # Ensures that results are returned as dictionaries
    )

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Dummy user database (replace with real DB query)
    users = {
        'admin': {'password': 'admin123', 'role': 'admin'},
        'user': {'password': 'user123', 'role': 'user'}
    }

    # Validate user credentials
    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_jwt(user_id=username, role=user['role'])
    return jsonify({'token': token}), 200

# Define a route for the home page
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Allotments Management System</title>
        <style>
            /* CSS styles for the homepage layout */
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }
            .container {
                text-align: center;
                background: #fff;
                padding: 20px 40px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                color: #0056b3;
            }
            p {
                font-size: 1.2rem;
                margin: 0;
            }
            .links {
                margin-top: 20px;
            }
            a {
                text-decoration: none;
                color: #0056b3;
                font-weight: bold;
                margin: 0 10px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Allotments Management System</h1>
            <p>Welcome to the API homepage.</p>
            <div class="links">
                <!-- Links to different sections of the API -->
                <a href="/departments">Departments</a>
                <a href="/sites">Sites</a>
                <a href="/residents">Residents</a>
                <a href="/rentals">Rentals</a>
                <a href="/allotments">Allotments</a>
            </div>
        </div>
    </body>
    </html>
    """

# Custom error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(error):
    # Return a JSON response with an error message and 400 status code
    return jsonify({"error": "Invalid JSON"}), 400


# ----------------------------------------------- Departments ------------------------------------------------
# Route to fetch all Departments
@app.route('/departments', methods=['GET'])  
@jwt_required()  # Any authenticated user can view
def get_departments():
    connection = None  

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Departments")  
            departments = cursor.fetchall()
        return jsonify(departments), 200

    except Exception as e:
        return jsonify({'Database connection error': str(e)}), 500

    finally:
        if connection:
            connection.close()

# Route to fetch a specific department by its ID
@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Departments WHERE Department_ID = %s", (id,))
            department = cursor.fetchone()
        if department:
            return jsonify(department), 200
        else:
            return jsonify({'error': 'Department not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to add a new department
@app.route('/departments', methods=['POST'])
@jwt_required(role='admin') # Restrict access to admin role
def add_department():
    data = request.json  # Get the data sent in the request
    required_fields = ['Managers_Name', 'Email_Address', 'Mobile_Cell_Phone_Number']

    # Check if all required fields are provided in the request data
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    other_details = data.get('Other_Details', None)  # Optional field

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Departments (Managers_Name, Email_Address, Mobile_Cell_Phone_Number, Other_Details) VALUES (%s, %s, %s, %s)",
                (data['Managers_Name'], data['Email_Address'], data['Mobile_Cell_Phone_Number'], other_details)
            )
            connection.commit()  
        return jsonify({'message': 'Department added successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to update an existing department by its ID
@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.json  
    required_fields = ['Managers_Name', 'Email_Address', 'Mobile_Cell_Phone_Number']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Departments WHERE Department_ID = %s", (id,))
            department = cursor.fetchone()
            
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            
            cursor.execute(
                "UPDATE Departments SET Managers_Name=%s, Email_Address=%s, Mobile_Cell_Phone_Number=%s WHERE Department_ID=%s",
                (data['Managers_Name'], data['Email_Address'], data['Mobile_Cell_Phone_Number'], id)
            )
            connection.commit()  
        
        return jsonify({'message': 'Department updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to delete a department by its ID
@app.route('/departments/<int:id>', methods=['DELETE'])
@jwt_required(role='admin')  # Only admins can delete
def delete_department(id):
    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Departments WHERE Department_ID = %s", (id,))
            department = cursor.fetchone()
            
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            
            cursor.execute("DELETE FROM Departments WHERE Department_ID = %s", (id,))
            connection.commit()  
        
        return jsonify({'message': 'Department deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# -------------------------------------------------- Sites ---------------------------------------------------
# Route to fetch all sites
@app.route('/sites', methods=['GET'])
def get_sites():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.Site_ID,
                    s.Other_Details,
                    d.Managers_Name,
                    d.Mobile_Cell_Phone_Number
                FROM 
                    Sites s
                JOIN 
                    Departments d 
                ON 
                    s.Department_ID = d.Department_ID
                """)
            sites = cursor.fetchall() 
        return jsonify(sites), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to fetch a specific site by its ID
@app.route('/sites/<int:id>', methods=['GET'])
def get_site(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Sites WHERE Site_ID = %s", (id,))
            site = cursor.fetchone()  

        if site:
            return jsonify(site), 200
        
        else:
            return jsonify({'error': 'Site not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to add a new site
@app.route('/sites', methods=['POST'])
def add_site():
    data = request.json  
    required_fields = ['Department_ID']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            cursor.execute(
                 """
                INSERT INTO Sites (Department_ID, Other_Details) 
                VALUES (%s, %s)
                """,
                (data['Department_ID'], data.get('Other_Details', None))
            )
            connection.commit()  
        
        return jsonify({'message': 'Site added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to update an existing site by its ID
@app.route('/sites/<int:id>', methods=['PUT'])
def update_site(id):
    data = request.json  

    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Sites WHERE Site_ID = %s", (id,))
            site = cursor.fetchone()
            
            if not site:
                return jsonify({'error': 'Site not found'}), 404
            
            cursor.execute(
                """
                UPDATE Sites 
                SET Department_ID = %s, Other_Details = %s
                WHERE Site_ID = %s
                """,
                (data.get('Department_ID'), data.get('Other_Details', None), id)
            )
            connection.commit()  
        return jsonify({'message': 'Site updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# Route to delete a site by its ID
@app.route('/sites/<int:id>', methods=['DELETE'])
def delete_site(id):
    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Sites WHERE Site_ID = %s", (id,))
            site = cursor.fetchone()

            if not site:
                return jsonify({'error': 'Site not found'}), 404
            
            cursor.execute("DELETE FROM Sites WHERE Site_ID = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Site deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        connection.close()

# -------------------------------------------------- Residents ------------------------------------------------
@app.route('/residents', methods=['GET'])
def get_residents():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Residents")
            residents = cursor.fetchall()
        return jsonify(residents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/residents/<int:id>', methods=['GET'])
def get_resident(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Residents WHERE Resident_ID = %s", (id,))
            resident = cursor.fetchone()
        if resident:
            return jsonify(resident), 200
        else:
            return jsonify({'error': 'Resident not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/residents', methods=['POST'])
def add_resident():
    data = request.json
    required_fields = ['Resident_Details', 'Date_First_Registered', 'Date_Of_Birth']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Residents (Resident_Details, Date_First_Registered, Date_Of_Birth) VALUES (%s, %s, %s)",
                (data['Resident_Details'], data['Date_First_Registered'], data['Date_Of_Birth'])
            )
            connection.commit()
        return jsonify({'message': 'Resident added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/residents/<int:id>', methods=['PUT'])
def update_resident(id):
    data = request.json

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Residents WHERE Resident_ID = %s", (id,))
            resident = cursor.fetchone()
            if not resident:
                return jsonify({'error': 'Resident not found'}), 404
            cursor.execute(
                "UPDATE Residents SET Resident_Details=%s, Date_First_Registered=%s, Date_Of_Birth=%s WHERE Resident_ID=%s",
                (data['Resident_Details'], data['Date_First_Registered'], data['Date_Of_Birth'], id)
            )
            connection.commit()
        return jsonify({'message': 'Resident updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/residents/<int:id>', methods=['DELETE'])
def delete_resident(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Residents WHERE Resident_ID = %s", (id,))
            resident = cursor.fetchone()
            if not resident:
                return jsonify({'error': 'Resident not found'}), 404
            cursor.execute("DELETE FROM Residents WHERE Resident_ID = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Resident deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# --------------------------------------------------- Rentals ----------------------------------------------------
@app.route('/rentals', methods=['GET'])
def get_rentals():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rentals")
            rentals = cursor.fetchall()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/rentals/<int:id>', methods=['GET'])
def get_rental(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rentals WHERE Rental_ID = %s", (id,))
            rental = cursor.fetchone()
        if rental:
            return jsonify(rental), 200
        else:
            return jsonify({'error': 'Rental not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/rentals', methods=['POST'])
def add_rental():
    data = request.json
    required_fields = ['Allotment_ID', 'Resident_ID', 'Date_Rented_From', 'Date_Rented_To']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Rentals (Allotment_ID, Resident_ID, Date_Rented_From, Date_Rented_To) VALUES (%s, %s, %s, %s)",
                (data['Allotment_ID'], data['Resident_ID'], data['Date_Rented_From'], data['Date_Rented_To'])
            )
            connection.commit()
        return jsonify({'message': 'Rental added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/rentals/<int:id>', methods=['PUT'])
def update_rental(id):
    data = request.json

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rentals WHERE Rental_ID = %s", (id,))
            rental = cursor.fetchone()
            if not rental:
                return jsonify({'error': 'Rental not found'}), 404
            cursor.execute(
                "UPDATE Rentals SET Allotment_ID=%s, Resident_ID=%s, Date_Rented_From=%s, Date_Rented_To=%s WHERE Rental_ID=%s",
                (data['Allotment_ID'], data['Resident_ID'], data['Date_Rented_From'], data['Date_Rented_To'], id)
            )
            connection.commit()
        return jsonify({'message': 'Rental updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/rentals/<int:id>', methods=['DELETE'])
def delete_rental(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Rentals WHERE Rental_ID = %s", (id,))
            rental = cursor.fetchone()
            if not rental:
                return jsonify({'error': 'Rental not found'}), 404
            cursor.execute("DELETE FROM Rentals WHERE Rental_ID = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Rental deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# ------------------------------------------------- Allotments -------------------------------------------------------
@app.route('/allotments', methods=['GET'])
def get_allotments():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Allotments")
            allotments = cursor.fetchall()
        return jsonify(allotments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/allotments/<int:id>', methods=['GET'])
def get_allotment(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Allotments WHERE Allotment_ID = %s", (id,))
            allotment = cursor.fetchone()
        if allotment:
            return jsonify(allotment), 200
        else:
            return jsonify({'error': 'Allotment not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/allotments', methods=['POST'])
def add_allotment():
    data = request.json
    required_fields = ['Site_ID', 'Allotment_Location', 'Size', 'Annual_Rental']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Allotments (Site_ID, Allotment_Location, Size, Annual_Rental) VALUES (%s, %s, %s, %s)",
                (data['Site_ID'], data['Allotment_Location'], data['Size'], data['Annual_Rental'])
            )
            connection.commit()
        return jsonify({'message': 'Allotment added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/allotments/<int:id>', methods=['PUT'])
def update_allotment(id):
    data = request.json

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Allotments WHERE Allotment_ID = %s", (id,))
            allotment = cursor.fetchone()
            if not allotment:
                return jsonify({'error': 'Allotment not found'}), 404
            cursor.execute(
                "UPDATE Allotments SET Site_ID=%s, Allotment_Location=%s, Size=%s, Annual_Rental=%s WHERE Allotment_ID=%s",
                (data['Site_ID'], data['Allotment_Location'], data['Size'], data['Annual_Rental'], id)
            )
            connection.commit()
        return jsonify({'message': 'Allotment updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/allotments/<int:id>', methods=['DELETE'])
def delete_allotment(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Allotments WHERE Allotment_ID = %s", (id,))
            allotment = cursor.fetchone()
            if not allotment:
                return jsonify({'error': 'Allotment not found'}), 404
            cursor.execute("DELETE FROM Allotments WHERE Allotment_ID = %s", (id,))
            connection.commit()
        return jsonify({'message': 'Allotment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
