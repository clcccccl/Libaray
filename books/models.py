from django.db import models
class Books(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    version = models.CharField(max_length=30)
    image_url = models.CharField(max_length=100)
    total = models.IntegerField()
    stock = models.IntegerField()
    price_type_id = models.IntegerField()
    type_id = models.IntegerField()
    address = models.CharField(max_length=30)
    #zambid = models.IntegerField()

class Book(models.Model):
    books_id = models.IntegerField()
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    state = models.IntegerField()
    #zambid = models.IntegerField()
    price = models.IntegerField()

class BookType(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    parent_code = models.CharField(max_length=30)
    total = models.IntegerField()
    child_code = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    def __unicode__(self):
	return u'%s ' % (self.name)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    books_id = models.IntegerField()
    user_name = models.CharField(max_length=20)
    comment_date = models.DateTimeField()
    type = models.IntegerField()

class Borrow(models.Model):
    books_id = models.IntegerField()
    isbn = models.CharField(max_length=20)
    user_id = models.IntegerField()
    borrow_date = models.DateTimeField()
    also_date = models.DateTimeField()
    security_code = models.CharField(max_length=10)
    state = models.IntegerField()
    payment = models.IntegerField()

# Create your models here.
