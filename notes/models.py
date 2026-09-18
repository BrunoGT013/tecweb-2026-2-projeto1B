from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='notes',
    )

    def __str__(self):
        return f'{self.id}. {self.title}'
