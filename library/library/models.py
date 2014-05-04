from django.db import models
import datetime
from PIL import Image
from django.contrib.auth.models import User


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True,default=datetime.datetime.now().date())
    image = models.ImageField(upload_to="uploaded")

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.image:
            return
        super(Book, self).save()
        image = Image.open(self.image.path)
        (width,height) = image.size

        th =120.0 
        if width > th:
            ratio = th /width

        size = ( int(width * ratio), int(height * ratio) )
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

class Borrow(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)  
    borrow_date = models.DateField(blank=True, null=True,default=datetime.datetime.now().date())
    return_date = models.DateField(blank=True, null=True)