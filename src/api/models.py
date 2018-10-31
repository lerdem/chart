from django.db import models


class RandomData(models.Model):
    date = models.DateField()
    value1 = models.IntegerField()
    value2 = models.IntegerField()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return '{} | {}'.format(self.value1, self.value2)
