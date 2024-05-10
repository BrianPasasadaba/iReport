from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from datetime import datetime
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from DT_model import preprocess_data, train_decision_tree_model, predict_category, category_id_map
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO



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

# Load dataset
data = pd.read_csv('CDRRMO-data.csv')

# Preprocess data
X, y = preprocess_data(data)

# Train decision tree model
clf, vectorizer, X_test, y_test = train_decision_tree_model(X, y)

# Make predictions on testing set
y_pred_test = [predict_category(clf, vectorizer, report) for report in X_test]

# Calculate accuracy score on testing set
accuracy_test = accuracy_score(y_test, y_pred_test)

# Calculate confusion matrix on testing set
conf_matrix_test = confusion_matrix(y_test, y_pred_test)

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

#Route for form page
@app.route('/incident_form')
def incident_form():
    return render_template('incident_form.html')

#Route for submitting form
@app.route('/submit_incident_form', methods=['POST'])
def submit_incident_form():
    # Access form data using request object
    full_name = request.form.get('name')
    contact_number = request.form.get('contact_number')
    location = request.form.get('location')
    # Extract latitude and longitude if needed
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    victims = request.form.get('victims')
    details = request.form.get('details')
    
    # Predict category
    predicted_category = predict_category(clf, vectorizer, details)
    
    # Map predicted category to category ID
    category_id = category_id_map.get(predicted_category)

    # Get current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Full Name:", full_name)
    print("Contact Number:", contact_number)
    print("Location:", location)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Estimated Number of Victims:", victims)
    print("Further Details:", details)
    
    # Insert data into MySQL database along with predicted category ID
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO reports (date_time, name, phone_number, location, latitude, longitude, estimate_victims, report_details, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (current_datetime, full_name, contact_number, location, latitude, longitude, victims, details, category_id))
    mysql.connection.commit()
    cur.close()
    # Prepare success message (optional)
    message = "Report Submitted! First Responders are on their way."

    # Return JSON response with success message
    return jsonify({'message': message})

@app.route('/accuracy', methods=['GET'])
def get_accuracy():
    return jsonify({'accuracy': accuracy_test})

@app.route('/confusion_matrix', methods=['GET'])
def get_confusion_matrix():
    # Plot confusion matrix
    def plot_confusion_matrix(conf_matrix, labels):
        plt.figure(figsize=(8, 6))
        sns.set(font_scale=1.2)
        sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt='g', xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()

    # Convert confusion matrix to PNG image
    cm_image = plot_confusion_matrix(conf_matrix_test, labels=category_id_map.keys())

    # Return PNG image as response
    return Response(cm_image, mimetype='image/png')

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
    # Fetch data with corresponding status value from MySQL database
    cur = mysql.connection.cursor()
    cur.execute("SELECT r.report_id, r.date_time, r.phone_number, r.name, r.location, r.latitude, r.longitude, r.estimate_victims, r.report_details, s.report_status FROM reports r JOIN status s ON r.status_id = s.status_id")
    reports = cur.fetchall()
    cur.close()
    
    # Pass data to template and render
    return render_template('admin/report.html', reports=reports)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)