from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/incident_form')
def incident_form():
    return render_template('incident_form.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


if __name__ == "__main__":
    app.run(debug=True)