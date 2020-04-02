# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bookshopapp.models import User, Book, Log
from .serializer import BookSerializer, UserSerializer, LogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

book = Book()
user = User()


# Create your views here.
class BookList(APIView):
    def get(self, request, format=None):
        serializer = BookSerializer(book.return_book(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BookSerializer(data=book.create_book(request))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewClass(APIView):

    """
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404
    """

    def get(self, request, id,  format=None):
        # serializer = BookSerializer(self.get_object(id))
        serializer = BookSerializer(Book.objects.get(id=id))
        return Response(serializer.data)

    def put(self, request, id, format=None):
        # serializer = BookSerializer(self.get_object(id), data=request.data)
        serializer = BookSerializer(Book.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        # self.get_object(id).delete()
        Book.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    def get(self, request, format=None):
        serializer = UserSerializer(user.get_users(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        for current_user in user.get_user_email():
            if current_user.email == request.data.get('email'):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewClass(APIView):

    """
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
    """

    def get(self, request, id, format=None):
        serializer = UserSerializer(User.objects.get(id=id))
        return Response(serializer.data)

    def put(self, request, id, format=None):
        for current_user in user.get_user_email():
            if current_user.email == request.data.get('email'):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # serializer = UserSerializer(self.get_object(id), data=request.data)
        serializer = UserSerializer(User.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        # self.get_object(id).delete()
        User.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchBook(APIView):
    def post(self, request, format=None):
        for u in User.objects.all():
            if u.email == request.data.get('email') and u.password == request.data.get('password'):
                serializer1 = BookSerializer(Book.objects.filter(title__contains=request.data.get('title').upper()),
                                             many=True)
                log_data = {
                    'keyword': request.data.get('title'),
                    'user': u.id,
                }
                serializer2 = LogSerializer(data=log_data)
                if serializer2.is_valid():
                    serializer2.save()
                    return Response(serializer1.data, status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
