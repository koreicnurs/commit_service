from celery import shared_task
import arrow
import requests

from commit_service.celery import app
from commits.models import Repository, Commit

gl_url = 'https://gitlab.com/api/v4/projects/{}/repository/commits'
gh_url = 'https://api.github.com/repos/{}/{}/commits'


@shared_task
def parsing_repositories():
    repos = Repository.objects.all()
    gl_repos = repos.filter(type='gitlab')
    gh_repos = repos.filter(type='github')
    for repo in gl_repos:
        url = gl_url.format(repo.project_id)
        res = requests.get(url)
        if res.status_code != 200:
            print(f'Fail to get commits of this Project id: {repo.project_id}')
            continue
        for commit in res.json():
            commit_time = arrow.get(commit["committed_date"])
            Commit.objects.get_or_create(
                repo=repo,
                sha=commit["id"],
                author=commit["author_name"],
                message=commit["message"],
                commit_time=commit_time.datetime,
            )
    for repo in gh_repos:
        url = gh_url.format(repo.author_name, repo.repository_name)
        res = requests.get(url)
        if res.status_code != 200:
            print(f'Fail to get commits of this Project')
            continue
        for commit in res.json():
            commit_time = arrow.get(commit["commit"]["author"]["date"])
            Commit.objects.get_or_create(
                repo=repo,
                sha=commit["sha"],
                author=commit["commit"]["author"]["name"],
                message=commit["commit"]["message"],
                commit_time=commit_time.datetime,
            )
