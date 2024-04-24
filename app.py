from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to establish database connection
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ifra@1234",
        database="project"
    )

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
def get_pets():
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data from the 'pets' table
    query = "SELECT * FROM pets"

    # Execute the query
    cursor.execute(query)

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
@app.route('/our_pets')
def our_pets():
    # Fetch pets data from the database
    pets_data = get_pets()
    return render_template('OurPets.html', pets=pets_data)

# Route for the index page
@app.route('/')
def landing():
    return render_template('landing.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

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
    # Fetch pet data based on the pet_id from the database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data for the specific pet
    query = "SELECT * FROM pets WHERE pet_id = %s"
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
    return render_template('form.html')

# Function to fetch admin data from the database
def get_admin_data():
    # Connect to MySQL database
    mysql_connection = connect_to_database()
    cursor = mysql_connection.cursor()

    # Query to select data from the 'admin' table
    query = "SELECT * FROM admin"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows of the result
    admin_data = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    mysql_connection.close()

    return admin_data

# Route to render the admin page with admin data
@app.route('/admin')
def admin():
    # Fetch admin data from the database
    admin_data = get_admin_data()
    return render_template('admin.html', admin=admin_data)

# Route to render the admin login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Get the username and email from the form
        username = request.form['username']
        email = request.form['email']

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Query to check if the username and email exist in the admin table
        query = "SELECT * FROM admin WHERE username = %s AND email = %s"
        cursor.execute(query, (username, email))
        admin = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if admin:
            # Admin login successful, redirect to admin dashboard
            return redirect(url_for('admin_dashboard'))
        else:
            # Admin login failed, render the login form with an error message
            error_message = "Invalid username or email. Please try again."
            return render_template('admin.html', message=error_message)
    else:
        # Render the admin login form
        return render_template('admin.html')

# Route to render the admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch data or perform any actions needed for the admin dashboard
    return render_template('admin_dash.html')

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

@app.route('/add_adopter_form')
def add_adopter_form():
    return render_template('add.html')
# Route to handle the submission of the add adopter form
@app.route('/add_adopter', methods=['POST'])
def add_adopter():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        # Insert the adopter data into the database
        insert_query = "INSERT INTO adopter (name, email) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, email))
        mysql_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        mysql_connection.close()

        return redirect(url_for('add_adopter_form'))  # Redirect to the add adopter form after submission

@app.route('/delete_adopter_form')
def delete_adopter_form():
    return render_template('delete.html')
@app.route('/delete_adopter', methods=['POST'])
def delete_adopter():
    if request.method == 'POST':
        adopter_id = request.form['adopter_id']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        # Delete the adopter from the database
        delete_query = "DELETE FROM adopter WHERE adopter_id = %s"
        cursor.execute(delete_query, (adopter_id,))
        mysql_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        mysql_connection.close()

        return redirect(url_for('delete_adopter_form'))  # Redirect to the delete adopter form after submission

@app.route('/add_pet_form')
def add_pet_form():
    return render_template('add_pet.html')

# Route to handle the submission of the add pet form
@app.route('/add_pet', methods=['POST'])
def add_pet():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        species = request.form['species']
        gender = request.form['gender']
        adoption_status = request.form['adoption_status']
        age = request.form['age']
        breed = request.form['breed']
        image = request.form['image']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        # Insert the pet data into the database
        insert_query = "INSERT INTO pets (category, name, species, gender, adoption_status, age, breed, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (category, name, species, gender, adoption_status, age, breed, image))
        mysql_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        mysql_connection.close()

        return redirect(url_for('add_pet_form'))  # Redirect to the add pet form after submission

@app.route('/delete_pet_form')
def delete_pet_form():
    return render_template('delete_pet.html')

# Route to handle the submission of the delete pet form
@app.route('/delete_pet', methods=['POST'])
def delete_pet():
    if request.method == 'POST':
        pet_id = request.form['pet_id']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        # Delete the pet from the database
        delete_query = "DELETE FROM pets WHERE pet_id = %s"
        cursor.execute(delete_query, (pet_id,))
        mysql_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        mysql_connection.close()

        return redirect(url_for('delete_pet_form'))  # Redirect to the delete pet form after submission

# Route to handle adopter form submission
@app.route('/submit_adopter_form', methods=['POST'])
def submit_adopter_form():
    if request.method == 'POST':
        # Fetch form data
        adopter_name = request.form['adopter-name']
        email = request.form['adopter-email']
        phone = request.form['adopter-phone']
        address = request.form['adopter-address']

        # Connect to MySQL database
        mysql_connection = connect_to_database()
        cursor = mysql_connection.cursor()

        # Insert form data into the adopter table
        adopter_query = "INSERT INTO adopter (adopter_name, email, cont_no, address) VALUES (%s, %s, %s, %s)"
        cursor.execute(adopter_query, (adopter_name, email, phone, address))
        adopter_id = cursor.lastrowid  # Get the ID of the newly inserted adopter

        # Get the pet ID from the URL parameter
        pet_id = request.args.get('pet_id')

        # Insert data into the adoption_procedure table
        adoption_query = "INSERT INTO adoption_procedure (pet_id, adopter_id, adoption_date) VALUES (%s, %s, CURDATE())"
        cursor.execute(adoption_query, (pet_id, adopter_id))

        # Commit changes and close connection
        mysql_connection.commit()
        cursor.close()
        mysql_connection.close()

        return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
