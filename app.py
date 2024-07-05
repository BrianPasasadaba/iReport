from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify, Response, send_file, make_response, send_from_directory
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, portrait, A4, LEGAL
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import textwrap
import base64
import os
import time
from clustering_model import load_data_and_train_model, predict_cluster_and_distance


app = Flask(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/uploads'

app.config['MYSQL_HOST'] = 'iReport.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'iReport'
app.config['MYSQL_PASSWORD'] = 'iReportpassword'
app.config['MYSQL_DB'] = 'iReport$cdrrmo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'b6Vs6>[L;pgZ26`$]>?V'

mysql = MySQL(app)

# Define User model
class User(UserMixin):
    def __init__(self, employee_id, password):
        self.employee_id = employee_id
        self.password = password

    def get_id(self):
        return self.employee_id

# Load dataset
data = pd.read_csv('CDRRMO-data.csv')

# Start of Decision Tree model
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

# Start of KMeans clustering model
# Extract report details from your loaded data (assuming 'Report Details' column)
report_details = data['Report Details']

# Train the models using the loaded report details
clusterVectorizer, kmeans = load_data_and_train_model(report_details)

# Callback to load user from session
@login_manager.user_loader
def load_user(employee_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM admins WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(user_data[5], user_data[7])  # employee_id is at index 5 and password is at index 7
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
    picture = request.form.get('picture')
    
    # Predict category
    predicted_category = predict_category(clf, vectorizer, details)

    # Predict cluster and distance
    predicted_cluster, distance_to_nearest_centroid = predict_cluster_and_distance(clusterVectorizer, kmeans, details)
    
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
    # Insert data with predicted cluster and distance
    cur.execute("INSERT INTO reports (date_time, name, phone_number, location, latitude, longitude, estimate_victims, report_details, pictures, category_id, cluster, cluster_distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (current_datetime, full_name, contact_number, location, latitude, longitude, victims, details, picture, category_id, predicted_cluster, distance_to_nearest_centroid))
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
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()

    # Convert confusion matrix to PNG image
    cm_image = plot_confusion_matrix(conf_matrix_test, labels=category_id_map.keys())

    # Return PNG image as response
    return Response(cm_image, mimetype='image/png')

@app.route('/save-image', methods=['POST'])
def save_image():
    try:
        # Get base64 image data from request
        image_data = request.json.get('image')

        # Strip off the data:image/jpeg;base64 header to get the raw base64 data
        base64_data = image_data.split(',')[1]

        # Decode base64 data
        image_binary = base64.b64decode(base64_data)

        # Generate unique filename (you can use UUID or timestamp-based names)
        filename = f'image_{int(time.time())}.jpeg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save image to static/uploads directory
        with open(filepath, 'wb') as f:
            f.write(image_binary)

        # Construct URL for the saved image
        image_url = f'/uploads/{filename}'

        # Return the URL of the saved image
        return jsonify({'imageUrl': image_url}), 200

    except Exception as e:
        print(f"Error saving image: {e}")
        return jsonify({'error': 'Failed to save image'}), 500
    
@app.route('/delete-image', methods=['POST'])
def delete_image():
    try:
        # Get image URL from request
        image_url = request.json.get('imageUrl')
        
        # Extract the filename from the URL
        filename = os.path.basename(image_url)
        
        # Construct the file path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists
        if os.path.exists(filepath):
            # Delete the file
            os.remove(filepath)
            return jsonify({'message': 'Image deleted successfully'}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404

    except Exception as e:
        print(f"Error deleting image: {e}")
        return jsonify({'error': 'Failed to delete image'}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/term_of_use')
def term_of_use():
    return render_template('term_of_use.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html') 

#Start of admin routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['employee_id']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM admins WHERE employee_id = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[7], password):
            user = User(user_data[5], user_data[7])
            login_user(user)
            return redirect(url_for('report'))
        else:
            flash('Invalid employee ID or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/analytics')
@login_required
def analytics():

    cursor = mysql.connection.cursor()
    
     # Query to get the valid coordinates
    coordinates_query = """
        SELECT latitude, longitude, category_id
        FROM reports
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
          AND latitude != 0 AND longitude != 0
    """
    cursor.execute(coordinates_query)
    coordinates_data = cursor.fetchall()

    coordinates = [{'lat': lat, 'lng': lng, 'category_id': category_id} for lat, lng, category_id in coordinates_data]

    cursor.close()

    return render_template('admin/analytics.html', coordinates=coordinates)

@app.route('/analytics/data', methods=['GET'])
@login_required
def analytics_data():
    cursor = mysql.connection.cursor()

    # Get query parameters
    month = request.args.get('month', None)
    year = request.args.get('year', None)

    # Build the WHERE clause based on selected month and year
    where_clause = ""
    if month and year:
        where_clause = f"WHERE MONTH(date_time) = {month} AND YEAR(date_time) = {year}"
    elif month:
        where_clause = f"WHERE MONTH(date_time) = {month}"
    elif year:
        where_clause = f"WHERE YEAR(date_time) = {year}"

    analytics_query = f"""
        SELECT
            CASE category_id
                WHEN 1 THEN 'Medical Emergency'
                WHEN 2 THEN 'Vehicular Accident'
                WHEN 3 THEN 'Other Emergency'
                ELSE 'Unknown'
            END AS category_name,
            COUNT(*) AS count
        FROM reports
        {where_clause}
        GROUP BY category_id
    """

    cursor.execute(analytics_query)
    analytics_data = cursor.fetchall()

    # Fetch labels and values from the query result
    labels = [row[0] for row in analytics_data] if analytics_data else []
    values = [int(row[1]) for row in analytics_data] if analytics_data else []

    cursor.close()

    # Return JSON response
    return jsonify({'labels': labels, 'values': values})


@app.route('/help')
@login_required
def help():
    return render_template('admin/help.html')

@app.route('/report')
@login_required
def report():
    # Fetch data with corresponding status value from MySQL database
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT r.report_id, r.date_time, r.phone_number, r.name, r.location, r.latitude, r.longitude, 
           r.estimate_victims, r.report_details, r.pictures, r.responder_report, r.cluster, r.cluster_distance, s.report_status, c.categories
    FROM reports r 
    JOIN status s ON r.status_id = s.status_id
    JOIN category c ON r.category_id = c.category_id
""")
    reports = cur.fetchall()
    cur.close()
    
    # Pass data to template and render
    return render_template('admin/report.html', reports=reports)

@app.route('/update_report', methods=['POST'])
def update_report():
    if request.method == 'POST':
        # Get form data
        report_id = request.form['reportId']
        responder_report = request.form['responder_report']
        status = request.form['status']

        # Update the corresponding entry in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE reports SET responder_report = %s, status_id = %s WHERE report_id = %s", (responder_report, status, report_id))
        mysql.connection.commit()
        cur.close()

        # Return a success response
        return jsonify({'success': True}), 200

@app.route('/report/print-pdf')
def print_report_pdf():
    # Fetch data from database (same as report() function)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT r.report_id, r.date_time, r.phone_number, r.name, r.location,
            r.responder_report, c.categories
        FROM reports r
        JOIN category c ON r.category_id = c.category_id
        WHERE r.status_id = 3
    """)
    reports = cur.fetchall()
    cur.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(LEGAL))

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_normal.alignment = 1  # Center alignment
    style_normal.fontSize = 18  # Set font size to 10

    # Create table data
    data = [["Report ID", "Date and Time", "Phone Number", "Name",
             "Location", "Details", "Category"]]
    for report in reports:
        wrapped_report = [textwrap.fill(str(value), width=30) for value in report]  # Adjust width as needed
        data.append(wrapped_report)

    # Define column widths and maximum widths
    col_widths = [1*inch, 1.5*inch, 1.5*inch, 2*inch, 2*inch, 2.5*inch, 1.5*inch]

    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Vertical alignment
        ("WORDWRAP", (0, 0), (-1, -1), True),
        ("MIN_ROW_HEIGHT", (0, 0), (-1, -1), 12),  # Set minimum row height
    ]

    table = Table(data, colWidths=col_widths, style=table_style)

    # Add spacer between title and table
    spacer = Spacer(1, 0.5*inch)  # Adjust the size of the spacer as needed

    elements = [Paragraph("Emergency Report", style=style_normal),spacer, table]

    doc.build(elements)

    buffer.seek(0)
    pdf_content = buffer.getvalue()

    response = make_response(pdf_content)
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    response.headers['Content-type'] = 'application/pdf'
    return response


@app.route('/report/print-individual/<int:report_id>')
def print_individual_report(report_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT r.report_id, r.date_time, r.phone_number, r.name, r.location,
               r.estimate_victims, r.report_details, r.responder_report, 
               s.report_status, c.categories
        FROM reports r
        JOIN status s ON r.status_id = s.status_id
        JOIN category c ON r.category_id = c.category_id
        WHERE r.report_id = %s
    """, (report_id,))
    report = cur.fetchone()
    cur.close()

    if not report:
        return "Report not found", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=portrait(A4))

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_title = styles["Title"]
    style_normal.alignment = 1  # Center alignment
    style_normal.fontSize = 16  # Set font size to 12

    # Adding additional spacing
    space_large = Spacer(1, 0.5*inch)
    space_small = Spacer(1, 0.2*inch)

    # Custom style for report details
    custom_style = ParagraphStyle(
        'Custom',
        parent=style_normal,
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=10,
        alignment=0  # Left alignment
    )

    elements = [
        Paragraph("Report Details", style=style_title),
        Spacer(1, 0.5*inch),
        KeepTogether([Paragraph(f"Report ID: {report[0]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Category: {report[9]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Report Status: {report[8]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Date and Time: {report[1]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Phone Number: {report[2]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Name: {report[3]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Location: {report[4]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Estimated Victims: {report[5]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        KeepTogether([Paragraph(f"Report Details: {report[6]}", style=custom_style)]),
        Spacer(1, 0.1*inch),
        
    ]

    if report[7]:  # Only add Responder Report if it is not null
        elements.append(KeepTogether([Paragraph(f"Responder Report: {report[7]}", style=custom_style)]))
        elements.append(Spacer(1, 0.2*inch))


    doc.build(elements)

    buffer.seek(0)
    pdf_content = buffer.getvalue()

    response = make_response(pdf_content)
    response.headers['Content-Disposition'] = f'attachment; filename=report_{report_id}.pdf'
    response.headers['Content-type'] = 'application/pdf'
    return response


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)