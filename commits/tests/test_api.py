from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from commits.models import Repository
from commits.serializers import RepositorySerializer, Commit, CommitSerializer


class RepositoriesTestCase(APITestCase):

    def test_get_list_repos(self):
        repo_1 = Repository.objects.create(type='github', url='https://github.com/Liazzz/my-first-blog',
                                           author_name='Liazzz', repository_name='my-first-blog')
        repo_2 = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms',
                                           project_id=155777)
        url = reverse('repositories_list')
        response = self.client.get(url)
        serializer_data = RepositorySerializer([repo_1, repo_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class CommitsTestCase(APITestCase):
    def setUp(self):
        self.repos = Repository.objects.create(type='github', url='https://github.com/Liazzz/my-first-blog',
                                               author_name='Liazzz', repository_name='my-first-blog')
        self.commit_1 = Commit.objects.create(repo=self.repos,
                                              sha='3c2ab2596de7c950ff6e8cfc528667e9da3ae01f',
                                              author='Liazzz', message='create project',
                                              commit_time='2020-10-09T10:59:00Z')
        self.commit_2 = Commit.objects.create(repo=self.repos,
                                              sha='3c2ab2596de7c950ff6e8cfc528667e9da3ae123',
                                              author='Liazzz', message='create project',
                                              commit_time='2020-10-09T10:59:00Z')

    def test_get_list_commits(self):
        url = reverse('commits_list')
        response = self.client.get(url)
        serializer_data = CommitSerializer([self.commit_1, self.commit_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
