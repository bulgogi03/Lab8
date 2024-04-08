from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.secret_key = 'ooga booga'
database = SQLAlchemy(app)

class student(database.Model):      #database for student accounts
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(80), nullable = False, unique = True)
    password = database.Column(database.String(120), nullable = False)
    firstname = database.Column(database.String(80), nullable = False)
    lastname = database.Column(database.String(80), nullable = False)

class teacher(database.Model):      #database for teacher accounts
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(80), nullable = False, unique = True)
    password = database.Column(database.String(120), nullable = False)
    firstname = database.Column(database.String(80), nullable = False)
    lastname = database.Column(database.String(80), nullable = False)

class admin(database.Model):        #database for admin accounts
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(80), nullable = False, unique = True)
    password = database.Column(database.String(120), nullable = False)
    firstname = database.Column(database.String(80), nullable = False)
    lastname = database.Column(database.String(80), nullable = False)

with app.app_context():
    database.create_all()

@app.route('/')
def start_page():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        studentName = student.query.filter_by(username=username).first()
        teacherName = teacher.query.filter_by(username=username).first()
        adminName = admin.query.filter_by(username=username).first()

        if studentName and studentName.password == password:
            return redirect(url_for('student_portal'))
        elif teacherName and teacherName.password == password:
            return redirect(url_for('teacher_portal'))
        elif adminName and adminName.password == password:
            return redirect(url_for('admin_portal'))

    return redirect(url_for('start_page'))

@app.route('/student')
def student_portal():
    return render_template('student.html')

@app.route('/teacher')
def teacher_portal():
    return render_template('teacher.html')

@app.route('/admin')
def admin_portal():
    return render_template('admin.html')

@app.route('/create_acc.html')
def create_page():
    return render_template('create_acc.html')

@app.route('/create_acc', methods=['POST'])
def create_account():
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    account_type = request.form['account_type']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    # Check if the username already exists
    if account_type == 'student':
        existing_user = student.query.filter_by(username=username).first()
    elif account_type == 'teacher':
        existing_user = teacher.query.filter_by(username=username).first()
    elif account_type == 'admin':
        existing_user = admin.query.filter_by(username=username).first()
    
    if existing_user:
        flash("Username already exists. Please choose a different username.", 'error')
        return redirect(url_for('create_acc.html'))

    # Create a new user account
    if account_type == 'student':
        new_user = student(username=username, password=password, firstname=firstname, lastname=lastname)
    elif account_type == 'teacher':
        new_user = teacher(username=username, password=password, firstname=firstname, lastname=lastname)
    elif account_type == 'admin':
        new_user = admin(username=username, password=password, firstname=firstname, lastname=lastname)
    # Add the new user to the database
    database.session.add(new_user)
    database.session.commit()

    flash("Account successfully created!", 'success')
    return redirect(url_for('start_page'))

if __name__ == '__main__':
    app.run(debug=True)
