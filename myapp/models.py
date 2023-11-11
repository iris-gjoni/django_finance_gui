from django.db import models
from django.utils.text import slugify
# Create your models here.


class UploadModel(models.Model):
    file = models.FileField(upload_to='uploads/')


class Statistic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    @property
    def data(self):
        return self.dataitem_set.all()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class DataItem(models.Model):
    # statistic = models.ForeignKey(Statistic)
    # value = models.PositiveIntegerField()
    # owner = models.CharField(max_length=200)
    pass