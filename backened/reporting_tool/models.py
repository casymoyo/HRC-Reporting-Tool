from django.db import models
from users.models import User


class ExcludedClient(models.Model):
    """
    A model which keeps the names of excluded clients for the data
    to be filtered
    """
    name = models.CharField(max_length=255)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reports(models.Model):
    """
    A model to keep the generated reports
    """
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='reports', max_length=100)
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date_created} -> {self.name}'


class RawCsvFile(models.Model):
    file = models.FileField(upload_to='raw_csv_files', max_length=255)
    date_created = models.DateField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date_created} ({self.file})'
