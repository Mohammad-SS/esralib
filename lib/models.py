# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db import models
import datetime
from django.utils import timezone
# for image fields
from PIL import Image
from django.urls import reverse

# All database and tables will be defined here .


# Categoury Model
# Each category will be one model that has Name ,
# i.e : Category.name = Poems
class Category(models.Model):
    name = models.CharField(max_length=110)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"pk": self.pk})

# Books Model
# each book will be one object of this model
# if a book is reserved or out , backData MUST be filled
# when a book is reserved , backDate will be automatically set for 24 hours from now .


class Book(models.Model):
    name = models.CharField(max_length=110)
    desc = models.CharField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='booksimage', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    documentNumber = models.CharField(max_length=15)
    idNumber = models.CharField(max_length=400)
    author = models.CharField(max_length=300)
    publisher = models.CharField(max_length=100)
    publishdate = models.CharField(max_length=50)
    version = models.CharField(max_length=100, null=True, blank=True)
    lang = models.CharField(max_length=20, null=True, blank=True)
    info = models.CharField(max_length=400, null=True, blank=True)
    st = [('reserved', 'Reserved'), ('available', 'Available'), ('out', 'out')]
    status = models.CharField(max_length=10, choices=st, default='available')
    backDate = models.DateTimeField(blank=True, default=timezone.now)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class User(models.Model):
    displayName = models.CharField(max_length=30)
    password = models.CharField(max_length=16)
    phone = models.CharField(max_length=11  , unique=True)
    identityNumber = models.CharField(max_length=10 , unique=True)
    reservedBooks = models.IntegerField(default=0)
    outBooks = models.IntegerField(default=0)
    address = models.TextField()
    balance = models.IntegerField(default=0)
    def __unicode__(self):
        return self.identityNumber + "(" + self.phone + ")"