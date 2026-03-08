from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'this_is_a_secret_key'
db = SQLAlchemy(app)
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    fname = db.Column(db.String(150), nullable=False)
    lname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    school = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), nullable=True)
   
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['log_in_email']
        password = request.form['log_in_password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return render_template('calendar.html')
        else:
            error = "Incorrect email or password."
            return render_template('log_in.html', error=error)
    return render_template('log_in.html')

@app.route('/', methods=['GET', 'POST'])
def sign():
    error = None
    
    if request.method == 'POST':
        fname = request.form.get('fname', '').strip()
        lname = request.form.get('lname', '').strip()
        email = request.form.get('sign_up_email', '').strip()
        school = request.form.get('school', '').strip()
        status = request.form.get('status')
        password = request.form.get('sign_up_password', '')
        confirm = request.form.get('confirm_password', '')

        if fname == "":
            error = "First name cannot be empty!"
        elif lname == "":
            error = "Last name cannot be empty!"
        elif email.count("@") != 1 or email.count(".") == 0:
            error = "Email is not valid!"
        elif User.query.filter_by(email=email).first():
            error = "Email is already registered"
        elif school == "":
            error = "School cannot be empty!"
        elif status is None:
            error = "Please select a status"
        elif password == "":
            error = "Password cannot be empty!"
        elif confirm == "":
            error = "Confirm password cannot be empty!"
        elif password != confirm:
            error = "Passwords do not match!"
        elif len(password) < 8:
            error = "Password must be at least 8 characters long!"
        else:
            new_user = User(fname=fname, lname=lname, email=email, school=school, status=status)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please log in.")
            return redirect(url_for('login'))

    return render_template('sign_up.html', error=error)

class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    year_group = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    join_code = db.Column(db.String(6), nullable=False)

@app.route('/create_class/', methods=['GET', 'POST'])
def create_class():
    error = None

    if request.method == 'POST':
        class_name = request.form.get('class_name', '')
        subject = request.form.get('subject', '')
        year_group = request.form.get('year_group', '')

        if class_name == "":
            error = "Class name cannot be empty!"
        elif subject == "":
            error = "Subject cannot be empty!"
        elif year_group == "":
            error = "Year group cannot be empty!"
        elif year_group.isdigit() == False:
            error = "Year group must be a number!"
        elif int(year_group) < 7 or int(year_group) > 13:
            error = "Year group must be between 7 and 13!"
        else:
            join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            new_class = Class(class_name=class_name, subject=subject, year_group=int(year_group), teacher_id=1, join_code=join_code)
            db.session.add(new_class)
            db.session.commit()
            return render_template('create_classes.html', message="Class created! Join code: " + join_code)

    return render_template('create_classes.html', error=error)

@app.route('/calendar/')
def calendar():
    return render_template('calendar.html')

@app.route('/view_classes/')
def classes():
    classes = Class.query.all()
    return render_template('view_classes.html', classes=classes)

@app.route('/tasks/')
def tasks():
    return render_template('tasks.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/settings/')
def settings():
    return render_template('settings.html')

@app.route('/assign/')
def assign():
    return render_template('assign.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)