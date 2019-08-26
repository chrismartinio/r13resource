import requests
from bs4 import BeautifulSoup
from models import GitRepo, GitUser, db

# Get request for lectures


def get_lectures():
    response = requests.get('http://curric.rithmschool.com/r13/lectures/')
    soup = BeautifulSoup(response.text)

    return soup


def parse_data(parsed_json):

    owner_url = parsed_json[0]['owner']['html_url']
    owner_name = parsed_json[0]['owner']['login']
    owner_avatar = parsed_json[0]['owner']['avatar_url']

    new_user = GitUser(owner_url=owner_url,
                       owner_name=owner_name,
                       owner_avatar=owner_avatar)

    db.session.add(new_user)
    db.session.commit()

    ## Parse repos
    for item in parsed_json:
        repo_name = item['name']
        repo_url = item['html_url']
        repo_created = item['created_at']
        repo_last_push = item['pushed_at']
        repo_git_url = item['git_url']
        repo_size = item['size']
        repo_owner = new_user.id

        new_repo = GitRepo(repo_name=repo_name,
                           repo_url=repo_url,
                           repo_created=repo_created,
                           repo_last_push=repo_last_push,
                           repo_git_url=repo_git_url,
                           repo_size=repo_size,
                           repo_owner=repo_owner)

        db.session.add(new_repo)

    db.session.commit()

    return 'user added'
