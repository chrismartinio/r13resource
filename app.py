from flask import Flask, render_template, redirect, request, jsonify
from models import db, connect_db, Lecture, GitUser
from data import get_lectures
from bs4 import BeautifulSoup
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

# Pull current lectures


@app.route('/lecture')
def reveal_lecture():
    soup = get_lectures()
    links = []
    titles = []

    for link in soup.find_all('a'):
        links.append('http://curric.rithmschool.com/r13/lectures/' +
                     link.get('href'))

    for link in links:
        if 'zip' in link:
            continue
        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        if (soup.title is None):
            continue
        else:
            titles.append(soup.title.string)

    lectures = Lecture.query.order_by(Lecture.title)
    return render_template('new.html',
                           titles=titles,
                           links=links,
                           lectures=lectures)


@app.route('/lectures')
def lecture_page():
    url = 'http://curric.rithmschool.com/r13/lectures/ajax/'
    return render_template('lecture.html', url=url)
