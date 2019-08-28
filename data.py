import requests
from bs4 import BeautifulSoup
from models import GitRepo, GitUser, db

# Get request for lectures


def get_lectures():
    response = requests.get('http://curric.rithmschool.com/r13/lectures/')
    soup = BeautifulSoup(response.text)

    return soup


def parse_data(parsed_json):

    owner_url = parsed_json[0]['actor']['url']
    owner_name = parsed_json[0]['actor']['login']
    owner_avatar = parsed_json[0]['actor']['avatar_url']

    new_user = GitUser(owner_url=owner_url,
                       owner_name=owner_name,
                       owner_avatar=owner_avatar)

    db.session.add(new_user)
    db.session.commit()

    for item in parsed_json:
        if item['type'] == 'PushEvent':
            repo_name = item['repo']['name']
            repo_url = item['repo']['url']
            repo_push = item['created_at']
            repo_owner = new_user.id
            commits = item['payload']['commits'][-1]

            new_repo = GitRepo(
                repo_name=repo_name,
                repo_url=repo_url,
                repo_push=repo_push,
                repo_commit=commits['message'],
                repo_owner=repo_owner)

            db.session.add(new_repo)

    db.session.commit()


def parse_data2(parsed_json):

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


def parse_data_update(parsed_json, user_id):

    user = GitUser.query.get(user_id)
    user.owner_url = parsed_json[0]['owner']['html_url']
    user.owner_name = parsed_json[0]['owner']['login']
    user.owner_avatar = parsed_json[0]['owner']['avatar_url']

    updated_user = GitUser(owner_url=user.owner_url,
                           owner_name=user.owner_name,
                           owner_avatar=user.owner_avatar)

    db.session.add(updated_user)
    db.session.commit()

    ## Parse repos
    for item in parsed_json:
        repo = GitRepo.query.get(item['id'])
        repo.repo_name = item['name']
        repo.repo_url = item['html_url']
        repo.repo_created = item['created_at']
        repo.repo_last_push = item['pushed_at']
        repo.repo_git_url = item['git_url']
        repo.repo_size = item['size']
        repo.repo_owner = user.id

        updated_repo = GitRepo(repo_name=repo.repo_name,
                               repo_url=repo.repo_url,
                               repo_created=repo.repo_created,
                               repo_last_push=repo.repo_last_push,
                               repo_git_url=repo.repo_git_url,
                               repo_size=repo.repo_size,
                               repo_owner=repo.repo_owner)

        db.session.add(updated_repo)

    db.session.commit()

    return 'user added'