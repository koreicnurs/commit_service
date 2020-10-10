from django.test import TestCase

from commits.models import Repository
from commits.serializers import RepositorySerializer


class RepositorySerializerTestCase(TestCase):

    def test_get_list_repos(self):
        repo_1 = Repository.objects.create(type='github', url='https://github.com/Liazzz/my-first-blog')
        repo_2 = Repository.objects.create(type='gitlab', url='https://gitlab.com/mayan-edms/mayan-edms')
        data = RepositorySerializer([repo_1, repo_2], many=True).data
        expected_data = [
            {
                'id': repo_1.id,
                'type': 'github',
                'url': 'https://github.com/Liazzz/my-first-blog',
            },
            {
                'id': repo_2.id,
                'type': 'gitlab',
                'url': "https://gitlab.com/mayan-edms/mayan-edms",
            },
        ]
        self.assertEqual(expected_data, data)
