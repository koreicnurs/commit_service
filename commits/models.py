from django.db import models

repo_url_help_text = 'В это поле необходим URL репозитория в следующем формате ' \
                     'https://github.com/author_name/repository_name'
project_id_help_text = 'Номер репозитория необходим для GitLab'
author_name_help_text = 'Автор репозитория необходим для GitHub'
repository_name = 'Название репозитория необходим для GitHub'


class Repository(models.Model):
    REPO_CHOICES = [
        ('gitlab', 'GitLab.com'),
        ('github', 'GitHub.com'),
    ]
    type = models.CharField('Тип репозитория', max_length=10, choices=REPO_CHOICES, null=False, blank=False)
    url = models.CharField('Путь', max_length=50, help_text=repo_url_help_text, blank=True)
    project_id = models.IntegerField('Project ID', help_text=project_id_help_text, null=True, blank=True)
    author_name = models.CharField('Владелец репозитория', max_length=50, help_text=author_name_help_text, blank=True,
                                   null=True)
    repository_name = models.CharField('Название репозитория', max_length=50, help_text=repository_name, blank=True,
                                       null=True)

    def __str__(self):
        return f'{self.get_type_display()} - {self.url}'

    class Meta:
        verbose_name = 'репозитория'
        verbose_name_plural = 'репозитории'


class Commit(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE, verbose_name='Репозитории')
    sha = models.CharField('Commit ID', max_length=50)
    author = models.CharField('Автор', max_length=50)
    message = models.CharField('Сообщение', max_length=100)
    commit_time = models.DateTimeField('Дата коммита')

    def __str__(self):
        return self.sha + self.message

    class Meta:
        ordering = ['-commit_time']
        verbose_name = 'коммит'
        verbose_name_plural = 'коммиты'
