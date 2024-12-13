from flask import Flask, jsonify, request
import pymysql 

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

# Departments
@app.route('/departments', methods=['GET'])  
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
def add_department():
    data = request.json  # Get the data sent in the request
    required_fields = ['Managers_Name', 'Email_Address', 'Mobile_Cell_Phone_Number']

    # Check if all required fields are provided in the request data
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Departments (Managers_Name, Email_Address, Mobile_Cell_Phone_Number) VALUES (%s, %s, %s)",
                (data['Managers_Name'], data['Email_Address'], data['Mobile_Cell_Phone_Number'])
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




if __name__ == '__main__':
    app.run(debug=True)
