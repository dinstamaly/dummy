from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Type(models.Model):
    type = models.CharField(max_length=80)

    def __str__(self):
        return self.type


class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})


class Column_m(models.Model):
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE
    )
    order = models.IntegerField()
    data_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    from_int = models.IntegerField(null=True, blank=True)
    to_int = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.schema} {self.name}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.schema.pk})


class DataSet(models.Model):
    STATUS = (
        ('Processing', 'Processing'),
        ('Ready', 'Ready')
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    num_row = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50, default='Processing', choices=STATUS
    )
    created = models.DateField(auto_now_add=True, null=True)
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return f'{self.schema} - {self.num_row}'

    def get_absolute_url(self):
        return reverse('data-set', kwargs={'pk': self.pk})

