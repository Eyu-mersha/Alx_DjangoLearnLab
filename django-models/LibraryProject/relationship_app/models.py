from django.db import models

# Create your models here.
from django.db import models

# Author model with a CharField for name
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Book model with a ForeignKey to Author
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Library model with ManyToManyField to Book
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# Librarian model with OneToOneField to Library
class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
