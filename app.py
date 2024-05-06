from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL



app = Flask(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cdrrmo'

app.config['SECRET_KEY'] = 'b6Vs6>[L;pgZ26`$]>?V'

mysql = MySQL(app)

# Define User model
class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_id(self):
        return self.email

# Callback to load user from session
@login_manager.user_loader
def load_user(email):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM admins WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(user_data[5], user_data[6])
    else:
        return None


@app.route('/')
def index():
    '''
    account = {
        'email': 'admin@cdrrmo.com',
        'password': 'Admin1234'
    }

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(account['password']).decode('utf-8')

    # Insert the new user into the database
    cursor = mysql.connection.cursor()
    query = "INSERT INTO admins (email, password) VALUES (%s, %s)"
    cursor.execute(query, (account['email'], hashed_password))
    mysql.connection.commit()
    cursor.close()
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
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM admins WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[6], password):
            user = User(user_data[5], user_data[6])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('analytics'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/analytics')
@login_required
def analytics():
    return render_template('admin/analytics.html')

@app.route('/announcement')
@login_required
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
@login_required
def report():
    return render_template('admin/report.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)