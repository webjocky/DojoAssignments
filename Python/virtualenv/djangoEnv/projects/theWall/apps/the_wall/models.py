# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Messages(models.Model):
    user_id = models.ForeignKey(Users)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    message_id = models.ForeignKey(Messages)
    user_id = models.ForeignKey(Users)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
