from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL configuration
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="clover07",
    database="Pet_Adoption"
)
cursor = mysql_connection.cursor()

# Create table for shelters
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shelters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        pet_id VARCHAR(255),
        shelter_mail VARCHAR(255),
        contact_number VARCHAR(255),
        contact_person VARCHAR(255),
        location VARCHAR(255)
    )
""")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shelter')
def shelter():
    return render_template('shelter.html')

@app.route('/index')
def our_pets():
    return render_template('our_pets.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/tara')
def tara():
    return render_template('tara.html')

@app.route('/Anu')
def anu():
    return render_template('Anu.html')

@app.route('/Chanda')
def chanda():
    return render_template('Chanda.html')

@app.route('/Ganesha')
def ganesha():
    return render_template('Ganesha.html')

@app.route('/Gulab')
def gulab():
    return render_template('Gulab.html')

@app.route('/Gopi')
def gopi():
    return render_template('Gopi.html')


if __name__ == '__main__':
    app.run(debug=True)
