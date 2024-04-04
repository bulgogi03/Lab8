from flask import Flask, redirect, url_for, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.Enum('admin', 'teacher', 'student'), nullable=False)

@app.route('/')
def start_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            account_type = user.account_type
            if account_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif account_type == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif account_type == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return "Invalid account type"
        else:
            return "Please enter correct username and password"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/admin/dashboard')
def admin_dashboard():
    return "Welcome to Admin Dashboard"

@app.route('/teacher/dashboard')
def teacher_dashboard():
    return "Welcome to Teacher Dashboard"

@app.route('/student/dashboard')
def student_dashboard():
    return "Welcome to Student Dashboard"
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)