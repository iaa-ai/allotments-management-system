from flask import Flask 
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


if __name__ == '__main__':
    app.run(debug=True)
