from ..models import User
import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:
    def test_is_email_registered(self):
        """
        user = User.objects.create(
            fname='prajyot', lname='pomannawar', email='prajyot@gmail',
            password='prajyot@123', mobile='9552566838'
        )
        """
        user = mixer.blend('bookshopapp.User', email='prajyot@gmail')
        assert user.is_email_registered == "prajyot@gmail"

    def test_is_book_costly(self):
        book = mixer.blend('bookshopapp.Book', price=3400)
        assert book.is_book_costly == True

    def test_is_keyword_searched(self):
        log = mixer.blend('bookshopapp.Log', keyword='c++')
        assert log.is_keyword_searched == "c++"
