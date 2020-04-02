# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)

    @classmethod
    def get_users(cls):
        return User.objects.all()

    @classmethod
    def get_specific_user(cls, id):
        return User.objects.get(id=id)

    def get_user_email(self):
        return User.objects.only('email')

    def get_user_pass(self):
        return User.objects.only('password')

    @property
    def is_email_registered(self):
        return self.email

    class Meta:
        db_table = "users"


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publication = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    isbn = models.IntegerField()
    price = models.IntegerField()

    @classmethod
    def return_book(cls):
        return Book.objects.all()

    @classmethod
    def return_specific_book(cls, id):
        return Book.objects.get(id=id)

    @classmethod
    def create_book(cls, request):
        data = {
            'title': request.data.get('title').upper(),
            'author': request.data.get('author'),
            'publication': request.data.get('publication'),
            'type': request.data.get('type'),
            'isbn': int(request.data.get('isbn')),
            'price': int(request.data.get('price')),
        }
        return data

    @property
    def is_book_costly(self):
        return self.price > 3000

    class Meta:
        db_table = "books"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)

    @property
    def is_keyword_searched(self):
        return self.keyword

    class Meta:
        db_table = "logs"