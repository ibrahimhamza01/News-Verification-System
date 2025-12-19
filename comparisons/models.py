from django.db import models

class Comparison(models.Model):
    id = models.IntegerField(primary_key=True)
    prompt = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt

class Articles(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    comparison_prompt = models.ForeignKey(Comparison, on_delete=models.CASCADE, related_name='articles')
    comparison = models.TextField()
    similarity = models.FloatField()
    link = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content