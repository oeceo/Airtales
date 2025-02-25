from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager

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
        user.isAdmin = True
        user.save(using=self._db)
        return user

# User table
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30) 

    objects = UserManager()

    def __str__(self):
        return self.username

# JournalEntry table
class JournalEntry(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    entry = models.CharField(max_length=350, null=False)
    isReported = models.BooleanField(default=False)

    class Meta:
        unique_together = ('userID', 'date')  # Ensures each user can only have one entry per date
        verbose_name_plural = 'Entries'

    def __str__(self):
        return f"{self.userID.username} - {self.date}"

# Users profile table
class Profile(models.Model):
    userID = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Profile of {self.userID.username}"

# Prompt Table
class Prompt(models.Model):
    date = models.DateField(primary_key=True)
    prompt = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"Prompt for {self.date}"

# Reported table
class Reported(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('userID', 'date')
        verbose_name_plural = 'Reported Entries'

    def __str__(self):
        return f"Report - {self.userID.username} on {self.date}"