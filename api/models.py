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
    class TaskStatus(models.TextChoices):
        IN_PROGRESS = "INP", "In progress"
        COMPLETED = "COM", "Completed"
        CANCELLED = "CNCL", "Cancelled"

    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=TaskStatus, default=TaskStatus.IN_PROGRESS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
