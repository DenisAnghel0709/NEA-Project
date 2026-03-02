#need to also check if email already exists in database
#store user details in database
        

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        log_in_email= request.form['log_in_email']
        log_in_password= request.form['log_in_password']
        if log_in_email == "":
                error= "Email cannot be empty!"
                return render_template('log_in.html',error=error)
        if log_in_email.count('@') != 1 or log_in_email.count('.') == 0:
                error= "Invalid email format!"
                return render_template('log_in.html',error=error)
        if log_in_password == "":
                error= "Password cannot be empty!"
                return render_template('log_in.html',error=error)
        if log_in_password == sign_up_password and log_in_email == sign_up_email:
                return render_template('calendar.html')
        else:
                error= "Incorrect email or password!"
                return render_template('log_in.html',error=error)
    return render_template('log_in.html')

@app.route('/', methods=['GET', 'POST'])
def sign():
    error=None
    if request.method == 'POST':
        print("done")
        fname= request.form['fname']
        if fname == "":
                error= "First name cannot be empty!"
                return render_template('sign_up.html',error=error)
        lname= request.form['lname']
        if lname == "":
                error= "Last name cannot be empty!"
                return render_template('sign_up.html',error=error)
        sign_up_email = request.form['sign_up_email']
        if sign_up_email == "":
                error= "Email cannot be empty!"
                return render_template('sign_up.html',error=error)
        if sign_up_email.count('@') != 1 or sign_up_email.count('.') == 0:
                error= "Invalid email format!"
                return render_template('sign_up.html',error=error)
        school= request.form['school']
        if school == "":
                error= "School cannot be empty!"
                return render_template('sign_up.html',error=error)
        sign_up_password= request.form['sign_up_password']
        if sign_up_password != request.form['confirm_password']:
                error= "Passwords do not match!"
                return render_template('sign_up.html',error=error)
        if len(sign_up_password) < 8:
                error= "Password must be at least 8 characters long!"
                return render_template('sign_up.html',error=error)
        return render_template('log_in.html',error="Successfully signed up!")
    return render_template('sign_up.html')


if __name__ == "__main__":
    app.run(debug=True)

