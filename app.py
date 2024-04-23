from flask import Flask, render_template, url_for, redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cdrrmo'

mysql = MySQL(app)


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/incident_form')
def incident_form():
    return render_template('incident_form.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

#Start of admin routes
@app.route('/login')
def admin_login():
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