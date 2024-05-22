from django.db import models


class ProcessingTime(models.Model):
    last_time = models.CharField(max_length=30, default=None)

    def __str__(self):
        return self.last_time