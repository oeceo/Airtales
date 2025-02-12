from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# User manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must provide a password")

        user = self.model(
            email=self.normalize_email(email),  # makes the email lowercase
            username=username,
        )
        user.set_password(password) # hashes the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# User table
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Email = models.EmailField(unique=True)
    Username = models.CharField(max_length=30, unique=True)
    Password = models.CharField(max_length=30) 

    objects = UserManager()

    def __str__(self):
        return self.Username

# JournalEntry table
class JournalEntry(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateField()
    Entry = models.CharField(max_length=350, null=False)
    IsReported = models.BooleanField(default=False)

    class Meta:
        unique_together = ('UserID', 'Date')  # Ensures each user can only have one entry per date

    def __str__(self):
        return f"{self.UserID.Username} - {self.Date}"

# Users profile table
class Profile(models.Model):
    UserID = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    Username = models.ForeignKey(User, to_field="Username", on_delete=models.CASCADE)
    Date = models.DateField()

    def __str__(self):
        return f"Profile of {self.Username}"

# Prompt Table
class Prompt(models.Model):
    Date = models.DateField(primary_key=True)
    Prompt = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"Prompt for {self.Date}"

# Reported table
class Reported(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateField()
    IsReported = models.ForeignKey(JournalEntry, to_field="IsReported", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('UserID', 'Date')

    def __str__(self):
        return f"Report - {self.UserID.Username} on {self.Date}"