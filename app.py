from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from oauthlib.oauth2 import WebApplicationClient
from flask_oauthlib.client import OAuth
app = Flask(__name__)
app.secret_key = '38984c9a11888697f6b274d3e52e8f53' 

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='497561493859-2l1rqnevoccrlti4hpnll1afqmlvkct1.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email profile openid', # Adjust the scope as needed
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


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
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google_authorized')
def google_authorized():
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    # Store the user's Google OAuth2 credentials in the session
    session['google_token'] = (response['access_token'], '')

    # Fetch user information from Google
    user_info = google.get('userinfo')
    return 'Logged in as: ' + user_info.data['email']

@google.tokengetter
def get_oauth_token():
    return session.get('google_token')
@app.route('/some_protected_route')
def some_protected_route():
    oauth_token = session.get('oauth_token')
    if oauth_token:
    
        api_response = make_authenticated_api_request(oauth_token)

        # Process the API response and return a result
        return 'API Response: {}'.format(api_response)
    else:
        # The user is not authenticated, handle accordingly
        return 'Access denied: User is not authenticated'

if __name__ == '__main__':
    app.run(debug=True)