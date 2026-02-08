from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=300)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"{self.user.username} — {self.question.text[:30]}"




