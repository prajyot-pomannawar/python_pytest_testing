import mock
import pytest
import json
from rest_framework import status
from django.urls import reverse
from ..models import User, Book
from ..serializer import UserSerializer, BookSerializer
from django.test import RequestFactory
from ..views import UserList, BookList, SearchBook
from django.test import TestCase, Client
from ..factories import BookFactory, UserFactory
from mock import Mock, patch
import requests

client = Client()
my_factory = RequestFactory()


@pytest.mark.django_db
@pytest.fixture
def create_book_using_factory():
    return BookFactory()


@pytest.mark.django_db
@pytest.fixture
def create_user_using_factory():
    return UserFactory()


@pytest.mark.django_db
@mock.patch('bookshopapp.models.Book.return_book', return_value=Book.objects.all())
def test_view_all_book(mock_get_book):
    """
    In this test case mocking is used by using decorators
    """
    response = client.get('/books')
    book_list = Book.objects.all()
    serializer = BookSerializer(book_list, many=True)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK
    assert mock_get_book.called is True


@pytest.mark.django_db
def test_view_single_book(create_book_using_factory):
    """
    In this test case mocking is used by using context manager.
    Model Instance is created using Factory
    """
    specific_book = create_book_using_factory
    response = client.get(reverse('view_single_book', kwargs={'id': specific_book.pk}))
    # book = Book.objects.get(id=self.first_book.pk)
    with mock.patch('bookshopapp.models.Book.return_specific_book',
                    return_value=Book.objects.get(id=specific_book.pk)):
        book = Book.objects.get(id=specific_book.pk)
    serializer = BookSerializer(book)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_book():
    """
    In this test case mocking is used by using context manager.
    """
    new_book = {
        'title': 'Aptitude', 'author': 'R S Agarwal', 'publication': 'Pune Prakashan',
        'type': 'aptitude', 'isbn': '111', 'price': '500'
    }
    path = reverse('create_book')
    with mock.patch('bookshopapp.models.Book.create_book', return_value=new_book):
        request = my_factory.post(path, json.dumps(new_book), content_type='application/json')
    response = BookList.as_view()(request).render()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_edit_book(create_book_using_factory):
    book1 = create_book_using_factory
    updated_book = {
        'title': 'Harry Potter', 'author': 'J. K. Rowling', 'publication': 'University of Exeter',
        'type': 'Story', 'isbn': '111', 'price': '5000'
    }
    response = client.put(reverse('edit_book', kwargs={'id': book1.pk}),
                          data=json.dumps(updated_book), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_delete_book(create_book_using_factory):
    book3 = create_book_using_factory
    response = client.delete(reverse('delete_book', kwargs={'id': book3.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@mock.patch('bookshopapp.models.User.get_users', return_value=User.objects.all())
def test_view_all_user(mock_get_user):
    """
    In this test case mocking is used by using decorators
    """
    response = client.get('/users')
    user_list = User.objects.all()
    serializer = UserSerializer(user_list, many=True)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK
    assert mock_get_user.called is True


@pytest.mark.django_db
def test_view_single_user(create_user_using_factory):
    """
    In this test case mocking is used by using context manager.
    Model Instance is created using Factory
    """
    specific_user = create_user_using_factory
    response = client.get(reverse('view_single_user', kwargs={'id': specific_user.pk}))
    with mock.patch('bookshopapp.models.User.get_specific_user',
                    return_value=User.objects.get(id=specific_user.pk)):
        user = User.objects.get(id=specific_user.pk)
    serializer = UserSerializer(user)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_user():
    new_user = {
        'fname': 'Ms', 'lname': 'Dhoni', 'email': 'dhoni@gmail', 'password': 'dhoni@123', 'mobile': '8776547888',
    }
    path = reverse('create_user')
    request = my_factory.post(path, json.dumps(new_user), content_type='application/json')
    response = UserList.as_view()(request).render()
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_edit_user(create_user_using_factory):
    user1 = create_user_using_factory
    updated_user = {
        'fname': 'Ms', 'lname': 'Dhoni', 'email': 'dhoni@gmail', 'password': 'dhoni@123', 'mobile': '8776547888',
    }
    response = client.put(reverse('edit_user', kwargs={'id': user1.pk}),
                          data=json.dumps(updated_user), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_delete_user(create_user_using_factory):
    user3 = create_user_using_factory
    response = client.delete(reverse('delete_user', kwargs={'id': user3.pk}))
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
