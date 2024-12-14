from faker import Faker
import mysql.connector
from random import randint

fake = Faker()

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bakanese",
    database="allotments"
)

cursor = db.cursor()


# Function to generate and insert data
def insert_data():
    # Lists to store generated IDs for later use in other tables
    department_ids = []
    site_ids = []
    allotment_ids = []
    resident_ids = []

    # Insert data into Departments table
    for _ in range(25):  # Generate 25 records
        manager_name = fake.name()
        email = fake.email()
        phone = "+63" + ''.join([str(fake.random_int(min=0, max=9)) for _ in range(9)])
        other_details = fake.sentence()
        cursor.execute("""
            INSERT INTO Departments (Managers_Name, Email_Address, Mobile_Cell_Phone_Number, Other_Details)
            VALUES (%s, %s, %s, %s)
        """, (manager_name, email, phone, other_details))
        department_ids.append(cursor.lastrowid)  # Capture the Department_ID for later use

    # Insert data into Sites table
    for _ in range(25):
        department_id = department_ids[randint(0, len(department_ids) - 1)]  # Randomly choose a Department_ID
        other_details = fake.sentence()
        try:
            cursor.execute("""
                   INSERT INTO Sites (Department_ID, Other_Details)
                   VALUES (%s, %s)
               """, (department_id, other_details))
            site_ids.append(cursor.lastrowid)  
        except mysql.connector.Error as err:
            print(f"Error inserting into Sites table: {err}")
            db.rollback()  

    # Insert data into Allotments table
    for _ in range(25):
        site_id = site_ids[randint(0, len(site_ids) - 1)]  
        location = fake.address()
        size = round(randint(50, 200) + fake.random_number(digits=2) / 100, 2)
        rental = round(randint(500, 3000) + fake.random_number(digits=2) / 100, 2)
        other_details = fake.sentence()
        cursor.execute("""
                INSERT INTO Allotments (Site_ID, Allotment_Location, Size, Annual_Rental, Other_Details)
                VALUES (%s, %s, %s, %s, %s)
            """, (site_id, location, size, rental, other_details))
        allotment_ids.append(cursor.lastrowid)  

    # Insert data into Residents table
    for _ in range(25):
        resident_details = fake.name()
        registration_date = fake.date_this_decade()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        gender = fake.random_element(elements=('Male', 'Female'))
        on_waiting_list = fake.boolean()
        other_details = fake.sentence()
        cursor.execute("""
                INSERT INTO Residents (Resident_Details, Date_First_Registered, Date_Of_Birth, Gender, On_Waiting_List_YN, Other_Details)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (resident_details, registration_date, birth_date, gender, on_waiting_list, other_details))
        resident_ids.append(cursor.lastrowid)  

    # Insert data into Rentals
    for _ in range(25):
        allotment_id = allotment_ids[randint(0, len(allotment_ids) - 1)]  
        resident_id = resident_ids[randint(0, len(resident_ids) - 1)]  
        rented_from = fake.date_this_year()
        rented_to = fake.date_this_year()
        other_details = fake.sentence()
        cursor.execute("""
                INSERT INTO Rentals (Allotment_ID, Resident_ID, Date_Rented_From, Date_Rented_To, Other_Details)
                VALUES (%s, %s, %s, %s, %s)
            """, (allotment_id, resident_id, rented_from, rented_to, other_details))

    db.commit()

insert_data()

cursor.close()
db.close()