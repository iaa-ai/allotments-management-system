from flask import Flask
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='bakanese',
        database='allotments',
        cursorclass=pymysql.cursors.DictCursor
    )


if __name__ == '__main__':
    app.run(debug=True)