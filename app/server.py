from flask import Flask, render_template, request, send_file
from flask_mail import Mail, Message
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

db = SQLAlchemy(app)
mail = Mail(app)
engine = db.get_engine()

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column('response_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(255))
    email = db.Column('email', db.String(255))  
    q1 = db.Column('q1', db.String(512))
    q2 = db.Column('q2', db.String(512))
    q3 = db.Column('q3', db.String(512))
    q4 = db.Column('q4', db.String(512))
    q5 = db.Column('q5', db.String(512))

    def __init__(self, name, email, q1, q2, q3, q4, q5):
        self.__tablename__ = 'responses'
        self.name = name
        self.email = email
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5

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

            data_values = Response(name, email, q1, q2, q3, q4, q5)
            db.session.add(data_values)
            db.session.commit()

            message = Message('Submission received', recipients = [email], reply_to = 'rajarsi3997@gmail.com')
            message.body = "Mail"
            message.html = "<html>"
            message.html += "<body style=\"align-items: center; justify-content: center; font-family: \"Segoe UI\", Arial, sans-serif; background-color: #ffffff;\">"
            message.html += "<div style=\"margin: 5px; font-weight: bold; background: #2575fc; background: -webkit-linear-gradient(left, #6a11cb, #2575fc);"
            message.html += "color: white; width: 70%; padding: 50px 60px 70px 60px; \"><h1>COVID - 19 QUESTIONARE SURVEY</h1>"
            message.html += "Thank you for contributing! Your response has been received successfully!<br>Your complete response details are given below:<br><br>"
            message.html += "Name: " + name + "<br>"
            message.html += "Email: <a style=\"color: #fff; text-decoration: none;\">" + email + "</a><br><br>"
            message.html += "Question 1: " + q1 + "<br><br>"
            message.html += "Question 2: " + q2 + "<br><br>"
            message.html += "Question 3: " + q3 + "<br><br>"
            message.html += "Question 4: " + q4 + "<br><br>"
            message.html += "Question 5: " + q5 + "<br><br><br>"
            message.html += "Regards,<br>Rajarsi Saha<br>"
            message.html += "<div style = \"opacity: 0.7;\">Developer<br>"
            message.html += "M: +91 89107 42101<br>E: <a style=\"color: #fff; text-decoration: none;\">rajarsi3997@gmail.com</a></div></body></html>"
            mail.send(message)

            msg = "Email sent & Record successfully added"
        except:
            msg = "Error in insert operation"
        finally:
            print("[INFO]: ", msg)
            return render_template("submit.php")

@app.route("/login", methods = ['GET'])
def login():
    return render_template("login.html")

@app.route("/login_check", methods = ['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    if str(username) == 'admin' and str(password) == 'admin':
        return render_template("logged_in.php")
    else:
        return render_template("fail_login.php")

@app.route("/create", methods = ['POST'])
def create():
    try:
        table_names = inspect(engine).get_table_names()
        if table_names == []:
            db.create_all()
            return render_template("success_create.php")
        else:
            return render_template("fail_create.php")
    except Exception as e:
        print("[ERROR]: ", e)

@app.route("/delete", methods = ['POST'])
def delete():
    try:
        table_names = inspect(engine).get_table_names()
        if not table_names == []:
            db.drop_all()
            return render_template("success_delete.php")
        else:
            return render_template("fail_delete.php")
    except Exception as e:
        print("[ERROR]: ", e)

@app.route("/download", methods=['POST'])
def download():
    try:
        table_names = inspect(engine).get_table_names()
        if not table_names == []:
            data = Response.query.all()
            data_list = []
            for row in data:
                data_list.append(row.__dict__)
            df = pd.DataFrame(data_list)
            try:
                df = df.drop(['_sa_instance_state'], axis = 1)
                df = df[['id', 'name', 'email', 'q1', 'q2', 'q3', 'q4', 'q5']]
            except Exception as e:
                print("[ERROR]: ", e)
            finally:
                return render_template('view.html', tables=[df.to_html()], titles = ['na', 'Responses'])
        else:
            return render_template("fail_download.php")
    except Exception as e:
        print("[ERROR]: ", e)

@app.route("/em_d", methods = ['GET'])
def em():
    try:
        table_names = inspect(engine).get_table_names()
        if not table_names == []:
            data = Response.query.all()
            data_list = []
            for row in data:
                data_list.append(row.__dict__)
            df = pd.DataFrame(data_list)
            try:
                df = df.drop(['_sa_instance_state'], axis = 1)
                df = df[['id', 'name', 'email', 'q1', 'q2', 'q3', 'q4', 'q5']]
            except Exception as e:
                print("[ERROR]: ", e)
            finally:
                message = Message('Data', recipients = ['rajarsi3997@gmail.com'], reply_to = 'rajarsi3997@gmail.com')
                message.body = 'Body'
                message.html = '<html><head></head><body>{0}</body></html>'.format(df.to_html())
                mail.send(message)
                return render_template('view.html', tables=[df.to_html()], titles = ['na', 'Responses'])
        else:
            return render_template("fail_download.php")
    except Exception as e:
        print("[ERROR]: ", e)

if __name__ == "__main__":
    app.run()