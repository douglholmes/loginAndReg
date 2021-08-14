from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt
from django.db.models.deletion import CASCADE
# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <2:
            errors['first_name'] = "First name must be at least two characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two character long"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email'])==0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"
        current_users = User.objects.filter(email = postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        if len(postData['password']) > 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['password_confirm']:
            errors['mismatch'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) ==0:
            errors['email'] = "Email must be entered"
        if len(postData['password']) == 0:
            errors['password'] = "Password must be entered"
        elif bcrypt.checkpw(postData['password'].encode(),existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)