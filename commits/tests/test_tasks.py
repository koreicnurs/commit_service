from unittest import mock

from django.test import TestCase

from commits.models import Repository, Commit
from commits.tasks import parsing_gitlab_repositories, parsing_github_repositories
from commits.tests.mock_data import gitlab_mock_data, github_mock_data


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://gitlab.com/api/v4/projects/155566/repository/commits':
        return MockResponse(gitlab_mock_data, 200)
    elif args[0] == 'https://api.github.com/repos/django/django/commits':
        return MockResponse(github_mock_data, 200)

    return MockResponse(None, 404)


class GitLabTestCase(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab(self, *args):
        repo = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms',
                                         project_id=155566)
        parsing_gitlab_repositories()
        commits = Commit.objects.filter(repo=repo).all()
        self.assertEqual(commits.count(), 3)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab_bad_response(self, *args):
        repo = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms',
                                         project_id=1551231)
        parsing_gitlab_repositories()
        commits = Commit.objects.filter(repo=repo).all()
        self.assertEqual(commits.count(), 0)


class GitHubTestCase(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab(self, *args):
        repo = Repository.objects.create(type='github', url='https://github.com/django/django',
                                         author_name='django', repository_name='django')
        parsing_github_repositories()
        commits = Commit.objects.filter(repo=repo).all()
        self.assertEqual(commits.count(), 2)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab_bad_response(self, *args):
        repo = Repository.objects.create(type='github', url='https://github.com/django/django',
                                         author_name='qwerty', repository_name='qwerty')
        parsing_github_repositories()
        commits = Commit.objects.filter(repo=repo).all()
        self.assertEqual(commits.count(), 0)
