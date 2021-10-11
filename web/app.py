from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from school.config import DEV_DB, PROD_DB
import os


app = Flask(__name__)
app.secret_key = "Secret Key"

if os.environ.get('DEBUG') == '1':
    app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB
else:
        app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)

    def __init__(self, name, email, age, gender):

        self.name = name
        self.email = email
        self.age = age
        self.gender = gender

#Database Create 
db.create_all()

#Read_All operation
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students = all_data)

#Create Operation
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']

        my_data = Data(name, email, age, gender)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Data Inserted Successfully")

        return redirect(url_for('Index'))

#Update Operation
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.age = request.form['age']
        my_data.gender = request.form['gender']

        db.session.commit()
        flash("Student Data Updated Successfully")

        return redirect(url_for('Index'))

#Delete Operation
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Detail Deleted Successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=os.environ.get('DEBUG') == '1')