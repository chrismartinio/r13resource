from flask import Flask, render_template, redirect, request, jsonify, \
    url_for, json
from models import GitRepo, GitUser, Lecture, Exercise, Resource, db, connect_db
from data import *
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
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    extras = Resource.query.order_by(Resource.title).all()
    return render_template('index.html',
                           lectures=lectures,
                           exercises=exercises,
                           extras=extras)


@app.route('/add-user')
def show_add_repo():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    return render_template('add-repo.html',
                           lectures=lectures,
                           exercises=exercises)


@app.route('/submit-user', methods=['POST'])
def add_git_user():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    extras = Resource.query.order_by(Resource.title).all()

    ## Check if user exists on Git
    username = request.json['username']
    git_data = requests.get(f'https://api.github.com/users/{username}/repos')

    ## Response if user not found
    if git_data.status_code == 404:
        return '404'
    
    elif git_data.status_code == 200:
        content = git_data.content
        parsed_json = json.loads(content)
        
        ## Parse data and add user
        parse_data(parsed_json)
        return '200'
    
    else:
        return '499'
    
    
        # return render_template('github-users.html',
        #                        gitusers=GitUser.query.all(),
        #                        gitrepos=GitRepo.query.all(),
        #                        lectures=lectures,
        #                        exercises=exercises,
        #                        extras=extras,
        #                        message=msg)

        #  return render_template('github-users.html',
        #                        message="user added successfully",
        #                        gitusers=GitUser.query.all(),
        #                        gitrepos=GitRepo.query.all(),
        #                        lectures=lectures,
        #                        exercises=exercises,
        #                        extras=extras)
  




    # url = f'https://api.github.com/users/{username}/repos'
    # new_user = GitUser(name=username, url=url)

    # db.session.add(new_user)
    # db.session.commit()

    # users = GitUser.query.all()

    # return redirect('/github-users')


@app.route('/github-repos')
def github_repos():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    gitusers = GitUser.query.all()
    gitrepos = GitRepo.query.all()
    extras = Resource.query.order_by(Resource.title).all()

    return render_template('github-users.html',
                           lectures=lectures,
                           exercises=exercises,
                           extras=extras,
                           gitusers=gitusers,
                           gitrepos=gitrepos)


@app.route('/lectures')
def show_lecture():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    lecture_id = int(request.args['id'])

    lecture_url = Lecture.query.get(lecture_id).url

    return render_template('lecture.html',
                           lectures=lectures,
                           exercises=exercises,
                           url=lecture_url)


@app.route('/resources')
def show_resources():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    extras = Resource.query.order_by(Resource.title).all()

    return render_template('resources.html',
                           lectures=lectures,
                           exercises=exercises,
                           extras=extras)


@app.route('/resources', methods=['POST'])
def submit_resource():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()

    title = request.json['title']
    url = request.json['url']

    new_resource = Resource(title=title, url=url)

    db.session.add(new_resource)
    db.session.commit()

    extras = Resource.query.all()
    return '200'


@app.route('/add-extra')
def show_add_extra_page():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    extras = Resource.query.order_by(Resource.title).all()

    return render_template('new-extra.html',
                           lectures=lectures,
                           exercises=exercises,
                           extras=extras)


@app.route('/github-repos')
def show_github_repos():
    lectures = Lecture.query.all()
    exercises = Exercise.query.all()
    extras = Resource.query.order_by(Resource.title).all()

    return render_template('github-repos.html',
                           lectures=lectures,
                           exercises=exercises,
                           extras=extras)


# @app.route('/lecture/<lecture_id>')
# def show_lecture(lecture_id):
#     lectures = Lecture.query.order_by(Lecture.title)
#     # lecture_url = Lecture.query.filter(Lecture.id == lecture_id)

#     return render_template('new.html')

# Pull current lectures

# @app.route('/lecture')
# def reveal_lecture():
#     soup = get_lectures()
#     links = []
#     titles = []

#     for link in soup.find_all('a'):
#         links.append('http://curric.rithmschool.com/r13/lectures/' +
#                      link.get('href'))

#     for link in links:
#         if 'zip' in link:
#             continue
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text)
#         if (soup.title is None):
#             continue
#         else:
#             titles.append(soup.title.string)

#     lectures = Lecture.query.order_by(Lecture.title)
#     return render_template('new.html',
#                            titles=titles,
#                            links=links,
#                            lectures=lectures,
#                            exercises=exercises)

# @app.route('/lectures')
# def lecture_page():

#     url = 'http://curric.rithmschool.com/r13/lectures/ajax/'
#     return render_template('lecture.html',
#                            url=url,
#                            exercises=exercises,
#                            lectures=lectures)
