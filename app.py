import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ...

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    about = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Student {self.firstname}>'
    
    

@app.route('/')
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)


@app.route('/<int:id>/read')
def read(id):
    student = Student.query.get_or_404(id)
    return render_template("read.html", student=student)

@app.route('/create', methods=('GET', 'POST'))
def create():
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        about = request.form['about']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          about=about)
        db.session.add(student)
        db.session.commit()
    
        return redirect(url_for('index'))
    

    return render_template("create.html")


@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        about = request.form['about']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.about = about

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("create.html", student=student)

@app.route('/<int:id>/delete',  methods=['POST'])
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port='8000')
