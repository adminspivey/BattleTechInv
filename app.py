from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miniatures.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# In-memory user storage
users = {}

# User model for login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Test user
users['test'] = User(id='test', username='test', password=generate_password_hash('password'))

# Miniature database model
class Miniature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    era = db.Column(db.PickleType, nullable=False)
    unit_type = db.Column(db.String(50), nullable=False)
    weight_class = db.Column(db.String(50), nullable=False)
    weapons = db.Column(db.PickleType, nullable=False)
    equipment = db.Column(db.PickleType, nullable=False)
    quantity = db.Column(db.Integer, default=1)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Placeholder - will be replaced with DB query
    return render_template('index.html', miniatures=[])

@app.route('/add_miniature', methods=['POST'])
@login_required
def add_miniature():
    return redirect(url_for('index'))

@app.route('/delete_miniature', methods=['POST'])
@login_required
def delete_miniature():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
