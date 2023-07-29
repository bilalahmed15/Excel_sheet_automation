from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Mock user data (for demonstration purposes)
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# Hardcoded user credentials
users = [
    User(1, 'hamza123', 'macarto123'),
]

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Load the user by ID (required by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        for user in users:
            if user.username == username and user.password == password:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('display_sheets'))

        return 'Invalid credentials. Please try again.'

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Hardcoded Google Sheets links
google_sheets = [
    {
        'name': 'Findleadsv2',
        'link': 'https://docs.google.com/spreadsheets/d/1sCxK20PGL-rPCAp-kTATXrDFUu2-G3dv7txJ3lKQhNI/edit#gid=0'
    },
    {
        'name': 'Monthly Breakdown_',
        'link': 'https://docs.google.com/spreadsheets/d/1BrF4nIxYa1YMYy-oMBT-vjUz6vfxFUkN/edit?rtpof=true#gid=377264296'
    },
    {
        'name': 'Projects and Prices',
        'link': 'https://docs.google.com/spreadsheets/d/1_kh4sUJUUSNGWEpocoYKJ-PSbqdx_W9q4Y4_DB4bvXw/edit#gid=1183444542'
    },
    {
        'name': 'Leads for huda',
        'link': 'https://docs.google.com/spreadsheets/d/12bNwAe9Jx80ZTIKPt4-3tQx7n2FYyls0UznX_J7GZmI/edit#gid=0'
    },
    {
        'name': 'Outreach Report',
        'link': 'https://docs.google.com/spreadsheets/d/1rGFz0OtMi3IOFRBdzNOfdutdp7DkUxkebQz71dhak24/edit#gid'
    },
    {
        'name': 'LinkedIn Groups',
        'link': 'https://docs.google.com/spreadsheets/d/1WAS5NL5T9bh49fXIdS80yJOIK7BDmAyuPoBlHE_q-5I/edit#gid'
    },
    {
        'name': 'Nuture leads - Response Check List',
        'link': 'https://docs.google.com/spreadsheets/d/1hr6nmMAem2tqInsuQexyuPDLjitIRXyG4IKWT8N8z4s/edit#gid'
    },
    {
        'name': 'Follow Ups',
        'link': 'https://docs.google.com/spreadsheets/d/1GGO-umio9d4axL9_3AfN2HJZECGOxZ9V2o1b35mAAYk/edit#gid=928572285'
    },
    {
        'name': 'Passwords',
        'link': 'https://docs.google.com/spreadsheets/d/1OF9wR7q8p-IS2acxV7BYWwN8LEN_b4SuihN95_rfX3o/edit#gid'
    },
]

# Route to display all the sheets
@app.route('/sheets')
@login_required
def display_sheets():
    return render_template('sheets.html', sheets=google_sheets, username=current_user.username)

# Route to open a specific sheet
@app.route('/open_sheet/<int:sheet_id>')
@login_required
def open_sheet(sheet_id):
    if 0 <= sheet_id < len(google_sheets):
        return redirect(google_sheets[sheet_id]['link'])
    return "Invalid sheet ID."

if __name__ == '__main__':
    app.run(debug=True)
