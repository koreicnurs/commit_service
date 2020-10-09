from django.contrib import admin

from commits.models import Repository, Commit


@admin.register(Repository)
class RepoAdmin(admin.ModelAdmin):
    list_display = ('get_type', 'url', 'project_id')

    def get_type(self, obj):
        return obj.get_type_display()


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ('repo', 'author', 'sha', 'message', 'commit_time')
