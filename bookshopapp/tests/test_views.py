import pytest
import json
from rest_framework import status
from django.urls import reverse
from ..models import User, Book
from ..serializer import UserSerializer, BookSerializer
from django.test import RequestFactory
from ..views import UserList, BookList, SearchBook
from django.test import TestCase, Client
from mock import Mock, patch
import requests

client = Client()


@pytest.mark.django_db
class TestBookView(TestCase):

    def setUp(self):
        self.first_book = Book.objects.create(
            title='Panipat', author='Vishwas Patil', publication='Mehta',
            type='History', isbn='111', price='550')
        self.second_book = Book.objects.create(
            title='Musafir', author='Achyut Godbole', publication='Saket',
            type='auto biography', isbn='222', price='800')
        self.third_book = Book.objects.create(
            title='Sherlock', author='Arthur Doyal', publication='UK Publish',
            type='Story', isbn='333', price='450')
        self.new_book = {
            'title': 'Aptitude', 'author': 'R S Agarwal', 'publication': 'Pune Prakashan',
            'type': 'aptitude', 'isbn': '111', 'price': '500'
        }
        self.updated_book = {
            'title': 'Harry Potter', 'author': 'J. K. Rowling', 'publication': 'University of Exeter',
            'type': 'Story', 'isbn': '111', 'price': '5000'
        }
        self.search_book = {
            'email': 'virat@gmail', 'password': 'virat@123', 'title': 'c++'
        }
        self.factory = RequestFactory()

    def test_view_all_book(self):

        response = client.get('/books')
        book_list = Book.objects.all()
        serializer = BookSerializer(book_list, many=True)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_200_OK

    def test_view_single_book(self):
        response = client.get(reverse('view_single_book', kwargs={'id': self.first_book.pk}))
        book = Book.objects.get(id=self.first_book.pk)
        serializer = BookSerializer(book)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_200_OK

    def test_create_book(self):
        path = reverse('create_book')
        request = self.factory.post(path, json.dumps(self.new_book), content_type='application/json')
        response = BookList.as_view()(request).render()
        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_book(self):
        response = client.put(reverse('edit_book', kwargs={'id': self.first_book.pk}),
                              data=json.dumps(self.updated_book), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_book(self):
        response = client.delete(reverse('delete_book', kwargs={'id': self.third_book.pk}))
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserView(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(
            fname='virat', lname='kohli', email='virat@gmail', password='virat@123', mobile='9881726838')
        self.second_user = User.objects.create(
            fname='rohit', lname='sharma', email='rohit@gmail', password='rohit@123', mobile='9552566838')
        self.third_user = User.objects.create(
            fname='shikhar', lname='dhavan', email='shikhar@gmail', password='shikhar@123', mobile='9552566838')
        self.new_user = {
            'fname': 'Ms', 'lname': 'Dhoni', 'email': 'dhoni@gmail', 'password': 'dhoni@123', 'mobile': '8776547888',
        }
        self.updated_user = {
            'fname': 'Ms', 'lname': 'Dhoni', 'email': 'dhoni@gmail', 'password': 'dhoni@123', 'mobile': '8776547888',
        }

        self.factory = RequestFactory()

    def test_view_all_user(self):
        response = client.get('/users')
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_200_OK

    def test_view_single_user(self):
        response = client.get(reverse('view_single_user', kwargs={'id': self.first_user.pk}))
        user = User.objects.get(id=self.first_user.pk)
        serializer = UserSerializer(user)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self):
        path = reverse('create_user')
        request = self.factory.post(path, json.dumps(self.new_user), content_type='application/json')
        response = UserList.as_view()(request).render()
        assert response.status_code == status.HTTP_201_CREATED

    def test_edit_user(self):
        response = client.put(reverse('edit_user', kwargs={'id': self.first_user.pk}),
                              data=json.dumps(self.updated_user), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_user(self):
        response = client.delete(reverse('delete_user', kwargs={'id': self.third_user.pk}))
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestSearchBook(TestCase):
    def setUp(self):
        self.first_user = User.objects.create(
            fname='virat', lname='kohli', email='virat@gmail', password='virat@123', mobile='9881726838')
        self.second_user = User.objects.create(
            fname='rohit', lname='sharma', email='rohit@gmail', password='rohit@123', mobile='9552566838')
        self.third_user = User.objects.create(
            fname='shikhar', lname='dhavan', email='shikhar@gmail', password='shikhar@123', mobile='9552566838')
        self.first_book = Book.objects.create(
            title='Panipat', author='Vishwas Patil', publication='Mehta',
            type='History', isbn='111', price='550')
        self.second_book = Book.objects.create(
            title='Musafir', author='Achyut Godbole', publication='Saket',
            type='auto biography', isbn='222', price='800')
        self.third_book = Book.objects.create(
            title='Sherlock', author='Arthur Doyal', publication='UK Publish',
            type='Story', isbn='333', price='450')

        self.search_book = {
            'email': 'virat@gmail', 'password': 'virat@123', 'title': 'c++'
        }
        self.factory = RequestFactory()

    def test_search_book(self):
        request = self.factory.post(reverse('search_book'), json.dumps(self.search_book),
                                    content_type='application/json')
        response = SearchBook.as_view()(request).render()
        assert response.status_code == status.HTTP_200_OK
