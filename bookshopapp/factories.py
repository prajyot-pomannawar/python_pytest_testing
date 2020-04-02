import factory
from faker import Factory
from .models import User, Book, Log

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    fname = faker.name()
    lname = faker.name()
    email = faker.email()
    password = faker.password()
    mobile = faker.random_number()


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = Book

    title = faker.word().upper()
    author = faker.name()
    publication = faker.name()
    type = faker.word()
    isbn = faker.pyint()
    price = faker.random_number()
