from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"({self.name}, {self.telegram_id})"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
