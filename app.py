from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'shunna@1234'

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ifra@1234",
        database="project"
    )

@app.route('/adhere',methods=['GET', 'POST'])
def login_page():
    # Check if user is already logged in, if yes, redirect to admin page
    # if session.get('logged_in'):
    #     return redirect(url_for('new_page'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the entered credentials
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            # If admin exists, set a session variable indicating the admin is logged in
            session['logged_in'] = True
            return redirect(url_for('new_page'))
        else:
            # If admin doesn't exist or credentials are incorrect, display a warning message
            return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html')

# Route for the admin page
@app.route('/admin')
def admin_page():
    # Check if the admin is logged in by checking the session variable
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('admin_login.html')  # Change 'admin_page.html' with your actual admin page template

# Route for the new page after successful login
@app.route('/new_page')
def new_page():
    return render_template('admin_dash.html')
# Route to handle displaying the join query result
@app.route('/notadopted_pets')
def not_adopted():
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Execute the join query
        query = """
        SELECT p.pet_id, p.name AS pet_name, p.species, p.gender
FROM pets p
LEFT JOIN adoption_procedure ap ON p.pet_id = ap.pet_id
WHERE p.adoption_status = 'Not Adopted' AND ap.pet_id IS NULL

        """
        cursor.execute(query)

        # Fetch all rows
        not_adopted_pets = cursor.fetchall()
    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()

    # Render the template with the fetched data
    return render_template('notadopted.html', not_adopted_pets=not_adopted_pets)


# Function to fetch adopted pets data from the view
def get_adopted_pets():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM adopted_pets_view")
    adopted_pets = cursor.fetchall()

    cursor.close()
    connection.close()

    return adopted_pets

# Route to render the adopted pets page with data from the view
@app.route('/adopted_pets')
def adopted_pets():
    adopted_pets_data = get_adopted_pets()
    return render_template('adopted_pets.html', adopted_pets=adopted_pets_data)


# Function to fetch shelter data from the database
def get_shelters():
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data from the 'shelter' table
    query = "SELECT * FROM shelter"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows of the result
    shelters = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return shelters

# Function to fetch pets data from the database
def get_pets(pet_id=None):
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    if pet_id is None:
        # Query to select all data from the 'pets' table
        query = "SELECT * FROM pets"
    else:
        # Query to select a specific pet by ID
        query = "SELECT * FROM pets WHERE pet_id = %s"

    # Execute the query
    if pet_id is None:
        cursor.execute(query)
    else:
        cursor.execute(query, (pet_id,))

    # Fetch all rows of the result
    pets = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return pets

# Function to fetch medical records data from the database based on pet_id
def get_medical_records(pet_id):
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select medical records data for the specified pet_id
    query = "SELECT * FROM medical_records WHERE pet_id = %s"
    cursor.execute(query, (pet_id,))
    medical_records = cursor.fetchall()

    # Print out the retrieved records for debugging
    print("Retrieved medical records:", medical_records)

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return medical_records

# Route to render the shelter page with shelter data
@app.route('/shelter')
def shelter():
    # Fetch shelter data from the database
    shelters = get_shelters()
    return render_template('shelter.html', shelters=shelters)

# Route to render the pets page with pets data

# Route to render the pets page with pets data filtered by category
@app.route('/our_pets')
def our_pets():
    # Get the category parameter from the query string
    category = request.args.get('category')

    if category:
        # Fetch pets data from the database filtered by category
        pets_data = get_pets_by_category(category)
    else:
        # Fetch all pets data from the database
        pets_data = get_pets()

    return render_template('OurPets.html', pets=pets_data, selected_category=category)

# Function to fetch pets data from the database filtered by category
def get_pets_by_category(category):
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select pets data from the 'pets' table filtered by category
    query = "SELECT * FROM pets WHERE category = %s"

    # Execute the query
    cursor.execute(query, (category,))

    # Fetch all rows of the result
    pets = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return pets


# Route for the index page
@app.route('/',methods=['GET'])
def landing():
    return render_template('index.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/delete')
def delete():
    return render_template('delete_pet.html')


# Route for the team page
@app.route('/team')
def team():
    return render_template('team.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for individual pet pages
@app.route('/pet/<int:pet_id>')
def pet_info(pet_id):
    # Fetch pet data based on the pet_id from the view
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data for the specific pet from the view
    query = "SELECT * FROM pet_info_view WHERE pet_id = %s"
    cursor.execute(query, (pet_id,))
    pet_data = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    # Render the individual pet page with the fetched data
    return render_template('pet_info.html', pet=pet_data)
# Route to render the medical records page for a pet
@app.route('/medical_records/<int:pet_id>')
def medical_records(pet_id):
    # Fetch medical records data for the specified pet_id
    medical_records_data = get_medical_records(pet_id)
    return render_template('medical_records.html', pet_id=pet_id, medical_records=medical_records_data)

# Route to render the adopter form
@app.route('/adopter_form')
def adopter_form():
   pet_id = request.args.get('pet_id')
   print("Received pet_id in adopter_form route:", pet_id)  # Debugging statement

   return render_template('form.html',pet_id=pet_id)



# Function to fetch adopter data from the database
def get_adopter_data():
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data from the 'adopter' table
    query = "SELECT * FROM adopter"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows of the result
    adopter_data = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return adopter_data

# Route to render the adopter page with adopter data
@app.route('/adopter')
def adopter():
    # Fetch adopter data from the database
    adopter_data = get_adopter_data()
    return render_template('adopter.html', adopter=adopter_data)

@app.route('/adopter_login', methods=['GET', 'POST'])
def adopter_login():
    if request.method == 'POST':
        # Get the username and email from the form
        name = request.form['name']
        email = request.form['email']

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Query to check if the username and email exist in the admin table
        query = "SELECT * FROM adopter WHERE name = %s AND email = %s"
        cursor.execute(query, (name, email))
        adopter = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if adopter:
            # Admin login successful, redirect to admin dashboard
            return redirect(url_for('adopter_dashboard'))
        else:
            # Admin login failed, render the login form with an error message
            error_message = "Invalid username or email. Please try again."
            return render_template('adopter.html', message=error_message)
    else:
        # Render the admin login form
        return render_template('adopter.html')
    
@app.route('/adopter_dashboard', methods=['GET', 'POST'])
def adopter_dashboard():
    # Fetch data or perform any actions needed for the admin dashboard
         return render_template('index.html')    



@app.route('/add_pet_form')
def add_pet_form():
    return render_template('add_pet.html')

# Route to handle the submission of the add pet form
# Route to handle the submission of the add pet form
@app.route('/add_pet', methods=['POST'])
def add_pet():
    if request.method == 'POST':
        # Extract pet information from the form
        category = request.form['category']
        name = request.form['name']
        species = request.form['species']
        gender = request.form['gender']
        age = request.form['age']
        breed = request.form['breed']
        image = request.form['image']
        in_date_of_visit = request.form['in_date_of_visit']
        in_medicines_or_vaccinations = request.form['in_medicines_or_vaccinations']
        in_diagnosis = request.form['in_diagnosis']
        in_dr_name = request.form['in_dr_name']
        in_dr_number = request.form['in_dr_number']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        try:
            # Insert the pet data into the database
            insert_query = "INSERT INTO pets (category, name, species, gender, age, breed, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (category, name, species, gender, age, breed, image))
            mysql_connection.commit()

            # Get the last inserted pet ID
            pet_id = cursor.lastrowid

            # Print out the parameters passed to the stored procedure
            print("Calling stored procedure with parameters:")
            print("Pet ID:", pet_id)
            print("Date of Visit:", in_date_of_visit)
            print("Medicines or Vaccinations:", in_medicines_or_vaccinations)
            print("Diagnosis:", in_diagnosis)
            print("Doctor's Name:", in_dr_name)
            print("Doctor's Number:", in_dr_number)

            # Call the stored procedure to update medical records
            update_medical_records_query = """
                CALL update_medical_records(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(update_medical_records_query, (pet_id, in_date_of_visit, in_medicines_or_vaccinations, in_diagnosis, in_dr_name, in_dr_number))
            mysql_connection.commit()

        except mysql.connector.Error as e:
            # Handle any errors and rollback changes
            print("Error:", e)
            mysql_connection.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            mysql_connection.close()

        return redirect(url_for('add_pet_form'))

@app.route('/delete_pet', methods=['POST'])
def delete_pet():
    if request.method == 'POST':
        pet_id = request.form['pet_id']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        try:
            # Delete medical records associated with the pet first
            delete_medical_query = "DELETE FROM medical_records WHERE pet_id = %s"
            cursor.execute(delete_medical_query, (pet_id,))
            mysql_connection.commit()

            # Then delete the pet
            delete_query = "DELETE FROM pets WHERE pet_id = %s"
            cursor.execute(delete_query, (pet_id,))
            mysql_connection.commit()

        except mysql.connector.Error as e:
            # Handle any errors and rollback changes
            print("Error:", e)
            mysql_connection.rollback()
        finally:
            # Close the cursor and database connection
            cursor.close()
            mysql_connection.close()

        return redirect(url_for('delete'))  # Redirect to the delete pet form after submission

# Route to handle adopter form submission
# Route to handle adopter form submission
@app.route('/submit_adopter_form', methods=['POST'])
def submit_adopter_form():
    if request.method == 'POST':
        # Fetch form data
        adopter_name = request.form['adopter-name']
        mail = request.form['adopter-email']
        phone = request.form['adopter-phone']
        address = request.form['adopter-address']
        pet_id = request.args.get('pet_id')  # Get pet_id from the URL parameter

        print("Received pet_id:", pet_id)  # Debugging message

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        try:
            # Insert form data into the adopter table
            adopter_query = "INSERT INTO adopters (adopter_name, mail, cont_no, address,pet_id) VALUES (%s, %s, %s, %s,%s)"
            cursor.execute(adopter_query, (adopter_name, mail, phone, address,pet_id))
            adopter_id = cursor.lastrowid  # Get the ID of the newly inserted adopter

            print("Inserted adopter with ID:", adopter_id)  # Debugging message

            # Update the adoption status of the corresponding pet in the pets table
            update_query = "UPDATE pets SET adoption_status = 'Adopted' WHERE pet_id = %s"
            cursor.execute(update_query, (pet_id,))

            print("Updated pet_id:", pet_id)  # Debugging message

            # Insert data into the adoption_procedure table
            adoption_query = "INSERT INTO adoption_procedure (pet_id, adopter_id, adoption_date) VALUES (%s, %s, CURDATE())"
            cursor.execute(adoption_query, (pet_id, adopter_id))

            print("Inserted into adoption_procedure with pet_id:", pet_id)  # Debugging message

            # Commit changes and close connection
            mysql_connection.commit()
        except mysql.connector.Error as e:
            # Handle any errors and rollback changes
            print("Error:", e)
            mysql_connection.rollback()
        finally:
            cursor.close()
            mysql_connection.close()

    # Redirect to a suitable page after successful adoption procedure
    return redirect(url_for('landing'))  # Change to appropriate URL

# Function to create the view
# Function to create the pet_info_view in the database


if __name__ == '__main__':
    app.run(debug=True)
