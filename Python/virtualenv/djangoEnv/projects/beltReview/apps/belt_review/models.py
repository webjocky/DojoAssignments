# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, IntegrityError
import bcrypt
import re


# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['name'] or len(postData['name']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid name')
        if not postData['alias'] or len(postData['alias']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid alias')
        if not postData['email'] or not re.match(
                r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                postData['email']
        ):
            results['status'] = False
            results['errors'].append('Please enter a valid email')
        if not postData['password'] or len(postData['password']) < 8:
            results['status'] = False
            results['errors'].append('Please enter a valid password')
        if postData['password'] != postData['passvalid']:
            results['status'] = False
            results['errors'].append('Passwords do not match')

        user = User.objects.filter(email=postData['email'])
        if results['status']:
            try:
                user = User.objects.create(
                    name=postData['name'],
                    alias=postData['alias'],
                    email=postData['email'],
                    password=(bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())))
                user.save()
                results['user'] = user
            except IntegrityError as e:
                results['status'] = False
                if 'UNIQUE constraint' in e.message:
                    results['errors'].append(
                        'That email is already registered.')
                else:
                    results['errors'].append(e.message)
        return results

    def loginVal(self, postData):
        results = {'status': True, 'user': None, 'errors': []}
        try:
            user = User.objects.get(email=postData['email'])
            if user.password == bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
                pass
            else:
                raise Exception()
        except:
            results['status'] = False
            results['errors'].append("Incorrect Username or Password")

        if results['status']:
            results['user'] = user
        return results


class BookManager(models.Manager):
    def addBookVal(self, postData):
        results = {'status': True, 'errors': [], 'book': None}
        if not postData['title']:
            results['status'] = False
            results['errors'].append('Please enter a valid title')
        if not postData['choseAuthor'] or not postData['addAuthor']:
            results['status'] = False
            results['errors'].append('Please choose or add a new Author')
        if not postData['review'] or len(postData['review']) < 10:
            results['status'] = False
            results['errors'].append(
                'Please leave a valid review (more than 10 characters)')
        if not postData['rating'] or postData['rating'] == 'none':
            results['status'] = False
            results['errors'].append('Please select a rating.')

        if postData['choseAuthor'] != 'none':
            author = postData['choseAuthor']
        else:
            author = postData['addAuthor']

        try:
            user = User.objects.get(id=postData['user_id'])
            author = Author.objects.create(name=author)
            author.save()
            book = Book.objects.create(
                title=postData['title'],
                author=author,
            )
            book.save()
            review = Review.objects.create(
                content=postData['review'],
                rating=postData['rating']
            )
            review.save()
            review.books.add(book)
            review.users.add(user)

        except IntegrityError as e:
            results['status'] = False
            results['errors'].append(e.message)

        if results['status']:
            results['book'] = book
        return results


class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.name + "\\" + self.alias + " - " + self.email + " - " + "Created: " + str(self.created_at)


class Book(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    author = models.ForeignKey('Author', related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

    def __str__(self):
        return self.title + " - " + "Created: " + str(self.created_at)


class Author(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + "Created: " + str(self.created_at)


class Review(models.Model):
    content = models.TextField(blank=False, null=False)
    rating = models.CharField(max_length=1)
    books = models.ManyToManyField('Book', related_name="reviews")
    users = models.ManyToManyField('User', related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content + " - " + str(self.rating) + ", " + str(self.users)
