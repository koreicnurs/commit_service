from rest_framework import serializers

from .models import Repository, Commit


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('id', 'type', 'url',)


class CommitSerializer(serializers.ModelSerializer):
    repo = RepositorySerializer()

    class Meta:
        model = Commit
        fields = '__all__'
