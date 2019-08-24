from flask import Flask, render_template, redirect, request, jsonify
from models import db, connect_db, Lecture, GitUser
import requests
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///r13'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def show_index():
    lectures = Lecture.query.order_by(Lecture.title)
    return render_template('index.html', lectures=lectures)


@app.route('/add-repo')
def show_add_repo():
    lectures = Lecture.query.order_by(Lecture.title)
    return render_template('add-repo.html', lectures=lectures)


@app.route('/submit-user', methods=['POST'])
def add_git_user():
    username = request.form['git_username']
    url = f'https://api.github.com/users/{username}/repos'
    new_user = GitUser(name=username, url=url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')


@app.route('/cohort-code')
def cohort_code():
    lectures = Lecture.query.order_by(Lecture.title)
    users = GitUser.query.all()
    gitusers = []

    for user in users:
        response = requests.get(f'https://api.github.com/users/{user.name}')
        gitusers.append(response.json())

    return render_template('cohort-code.html',
                           lectures=lectures,
                           users=gitusers)


# @app.route('/lecture/<lecture_id>')
# def show_lecture(lecture_id):
#     lectures = Lecture.query.order_by(Lecture.title)
#     # lecture_url = Lecture.query.filter(Lecture.id == lecture_id)

#     return render_template('new.html')


@app.route('/lecture')
def reveal_lecture():
    lectures = Lecture.query.order_by(Lecture.title)
    return render_template('new.html', lectures=lectures)
