import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def total_votes(self):
        return sum(choice.votes for choice in self.choice_set.all())  # Soma os votos de todas as respostas

    def has_votes(self):
        return any(choice.votes > 0 for choice in self.choice_set.all())  # Verifica se há pelo menos um voto


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
