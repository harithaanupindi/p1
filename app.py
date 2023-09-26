from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure your SQLAlchemy database URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hillgrange@localhost:5433/Registration'  # Database name is "Registration"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define your models
class Registration(db.Model):
    __tablename__ = 'registration'
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
        registration = Registration(name=name, email=email, phone=phone)

        try:
            db.session.add(registration)
            db.session.commit()
            return redirect(url_for('thank_you'))  # Redirect to the thank you page
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return "An error occurred while saving the data."

    # Handle GET requests or errors by rendering the registration form again
    return render_template('registrations.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)