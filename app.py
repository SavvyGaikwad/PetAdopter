from flask import Flask, render_template
import mysql.connector
from project_credentials import host, user, password, database


app = Flask(__name__)

# MySQL configuration


# Route to fetch pets data from the database
@app.route('/our_pets')
def our_pets():
    # Fetch pets data from the database
    cursor.execute("SELECT * FROM pets")
    pets_data = cursor.fetchall()
    return render_template('OurPets.html', pets=pets_data)

if __name__ == '__main__':
    app.run(debug=True)
