from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from user import User

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cdrrmo'

app.config['SECRET_KEY'] = 'b6Vs6>[L;pgZ26`$]>?V'

mysql = MySQL(app)


@app.route('/')
def index():
    '''
    # Check if a user already exists in the database (optional)
    existing_user = User.get_by_email('admin@cdrrmo.com', mysql)  # Replace with desired email

    if not existing_user:
        # Create a new user with a strong password (replace with your desired password)
        new_user = User('admin@cdrrmo.com', 'Admin123')  # Removed generate_password_hash

        # Insert the new user into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO admins (email, password) VALUES (%s, %s)', (new_user.email, new_user.password_hash))
        mysql.connection.commit()

        flash('User created successfully!', 'success')
    else:
        flash('User already exists!', 'info')  # Or handle existing user differently
    '''

    return render_template('index.html')

@app.route('/incident_form')
def incident_form():
    return render_template('incident_form.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

#Start of admin routes
@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.get_by_email(email, mysql)

        print("Fetched user:", user)  # Print the retrieved user object

        if user:  # Check if user is found
            print("Verifying password...")
            if user.verify_password(password):
                print("Login successful!")
                session['logged_in'] = True
                session['email'] = email
                flash('Login successful!', 'success')
                return redirect(url_for('analytics'))  # Redirect to your desired route
            else:
                print("Login failed: Invalid password.")
                flash('Invalid email or password.', 'danger')
        else:
            print("Login failed: User not found.")
            flash('Invalid email or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/analytics')
def analytics():
    return render_template('admin/analytics.html')

@app.route('/announcement')
def announcement():
    return render_template('admin/announcement.html')

@app.route('/detail_report')
def detail_report():
    return render_template('admin/detail_report.html')

@app.route('/adminfaqs')
def admin_faqs():
    return render_template('admin/faqs.html')

@app.route('/faqs_add')
def faqs_add():
    return render_template('admin/faqs_add.html')

@app.route('/help')
def help():
    return render_template('admin/help.html')

@app.route('/report')
def report():
    return render_template('admin/report.html')

@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)