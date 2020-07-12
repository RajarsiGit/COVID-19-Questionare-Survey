from flask import Flask, render_template, request, send_file
from flask_mail import Mail, Message
import sqlite3 as sql
import csv
import requests
import os

secret_key = str(os.urandom(24))
app = Flask(__name__)

app.config['TESTING'] = False
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'deployment'
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = 'rajarsi3997@gmail.com'
app.config['MAIL_USERNAME'] = 'rajarsi3997@gmail.com'
app.config['MAIL_PASSWORD'] = 'nhdzeykclnnhkrau'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/", methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/submit", methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        try:
            first_name = request.form['q3_fullName3[first]']
            last_name = request.form['q3_fullName3[last]']
            name = str(first_name) + " " + str(last_name)
            email = str(request.form['q6_email6'])
            q1 = str(request.form['q11_whatare'])
            q2 = str(request.form['q12_whatcouldYou'])
            q3 = str(request.form['q15_whatwouldYou15'])
            q4 = str(request.form['q16_whatAre'])
            q5 = str(request.form['q17_anyOther'])

            connection = sql.connect("database.db")
            cursor = connection.cursor()
            data = (name, email, q1, q2, q3, q4, q5)
            query = "INSERT INTO data (name, email, q1, q2, q3, q4, q5) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, data)
            connection.commit()

            message = Message('Submission received', recipients = [email], reply_to = 'rajarsi3997@gmail.com')
            message.body = "Mail"
            message.html = "<html>"
            message.html += "<body style=\"align-items: center; justify-content: center; font-family: \"Segoe UI\", Arial, sans-serif; background-color: #ffffff;\">"
            message.html += "<div style=\"margin: 5px; font-weight: bold; background: #2575fc; background: -webkit-linear-gradient(left, #6a11cb, #2575fc);"
            message.html += "color: white; width: 70%; padding: 50px 60px 70px 60px; \"><h1>COVID - 19 QUESTIONARE SURVEY</h1>"
            message.html += "Thank you for contributing! Your response has been received successfully!<br>Your complete response details are given below:<br><br>"
            message.html += "Name: " + name + "<br>"
            message.html += "Email: <a style=\"color: #fff; text-decoration: none;\">" + email + "</a><br>"
            message.html += "Question 1: " + q1 + "<br>"
            message.html += "Question 2: " + q2 + "<br>"
            message.html += "Question 3: " + q3 + "<br>"
            message.html += "Question 4: " + q4 + "<br>"
            message.html += "Question 5: " + q5 + "<br><br><br>"
            message.html += "Regards,<br>Rajarsi Saha<br>"
            message.html += "<div style = \"opacity: 0.7;\">Developer<br>"
            message.html += "M: +91 89107 42101<br>E: <a style=\"color: #fff; text-decoration: none;\">rajarsi3997@gmail.com</a></div></body></html>"
            mail.send(message)

            msg = "Email sent & Record successfully added"
        except:
            connection.rollback()
            msg = "Error in insert operation"
        finally:
            #print("[INFO]: ", msg)
            return render_template("submit.php")
            connection.close()

@app.route("/login", methods = ['GET'])
def login():
    return render_template("login.html")

@app.route("/loggin_check", methods = ['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    if str(username) == 'admin' and str(password) == 'admin':
        return render_template("logged_in.php")
    else:
        return render_template("fail_login.php")

@app.route("/create", methods = ['POST'])
def create():
    connection = sql.connect("database.db")
    try:
        connection.execute('CREATE TABLE data (name TEXT, email TEXT, q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT)')
        return render_template("success_create.php")
    except Exception as e:
        return render_template("fail_create.php")

@app.route("/download", methods=['POST'])
def download():
    connection = sql.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("select * from data")
    with open("data.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    connection.close()
    return send_file(app.root_path + "/data.csv", as_attachment=True)

if __name__ == "__main__":
	app.run()