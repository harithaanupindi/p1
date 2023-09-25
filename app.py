from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure your SQLAlchemy database URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hillgrange@localhost:5433/Register'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define your models
class Register(db.Model):
    __tablename__ = 'register'  # Specify the table name explicitly
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

# Initialize the Migrate object correctly
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Create a Registration instance and add it to the database
        registration = Register(name=name, email=email, phone=phone)

        try:
            db.session.add(registration)
            db.session.commit()
            return redirect(url_for('thank_you'))
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return "An error occurred while saving the data."

    return render_template('registrations.html')

@app.route('/thank_you')
def thank_you():
    return "Thank you for registering!"

if __name__ == '__main__':
    app.debug = True
    app.run()
