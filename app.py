import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from check_connection import CheckConnection

db_connection =  "postgresql://postgres:postgres@172.17.0.2:5432/postgres" # teste container
print(db_connection)
# db_connection = "postgresql://postgres:toalha28@localhost:5432/ac5" # teste local
sql_connection = db_connection.replace("/postgres","")

conn_check = CheckConnection(connection_test= db_connection, sql_connection=sql_connection)
conn_check.check_connection()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_connection
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = "tb_student_danilo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ra = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    def __init__(self, ra, name, email):
        self.ra = ra
        self.name = name
        self.email = email

@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        student = Student(request.form['ra'],
                        request.form['nome'],
                        request.form['email'],
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.nome = request.form['nome']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', student = student)

if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host= "127.0.0.1", port=port, debug=True)
    