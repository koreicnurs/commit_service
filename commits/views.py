from rest_framework import generics

from .models import Repository, Commit
from .serializers import RepositorySerializer, CommitSerializer


class RepositoryListView(generics.ListAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class CommitListView(generics.ListAPIView):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
