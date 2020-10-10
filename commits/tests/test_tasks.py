from unittest import mock

from django.test import TestCase

from commits.models import Repository, Commit
from commits.tasks import parsing_gitlab_repositories
from commits.tests.mock_data import gitlab_mock_data


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://gitlab.com/api/v4/projects/155566/repository/commits':
        return MockResponse(gitlab_mock_data, 200)
    elif args[0] == 'https://api.github.com/repos/Liazzziazzz//commits':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


class GitLabTestCase(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab(self, *args):
        repos = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms',
                                          project_id=155566)
        parsing_gitlab_repositories()
        commits = Commit.objects.filter(repo=repos).all()
        self.assertEqual(commits.count(), 3)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_gitlab_bad_response(self, *args):
        repos = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms',
                                          project_id=1551231)
        parsing_gitlab_repositories()
        commits = Commit.objects.filter(repo=repos).all()
        self.assertEqual(commits.count(), 0)
