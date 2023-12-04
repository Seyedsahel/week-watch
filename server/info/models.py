from django.db import models

class HistoryRecord(models.Model):
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.link
