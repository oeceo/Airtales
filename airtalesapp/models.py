from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

class UserManager(BaseUserManager):
    def get_or_create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must provide a password")


        # try:
        #     user = self.get(email=self.normalize_email(email))
        #     created = False
        #     print("User already exists")
        # except User.DoesNotExist:
        #     # If the user doesn't exist, create one
        #     user = self.model(email=self.normalize_email(email), username=username)
        #     print("Raw password:", user.password)
        #     user.set_password(password)  # Hash the password
        #     print("Password hashed:", user.password)
        #     # user.save(using=self._db)
        #     user.save()
        #     created = True


        user, created = self.get_or_create(
            email=self.normalize_email(email),
            defaults={"username": username}
        )
        if created:
            user.set_password(password)  # Hashes the password
            user.save(using=self._db)
            print("password set and user saved")
            Profile.objects.get_or_create(userID=user)

        # Create profile only if a new user was created
        # if created:
        #     Profile.objects.get_or_create(userID=user)

        return user

    def create_superuser(self, email, username, password):
        user = self.get_or_create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# User table
class User(AbstractBaseUser, PermissionsMixin):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    #REQUIRED_FIELDS = []
    def __str__(self):
        return self.username

# Users profile table
class Profile(models.Model):
    userID = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    #date = models.DateField()

    def __str__(self):
        return f"Profile of {self.userID.username}"

# Prompt Table
class Prompt(models.Model):
    date = models.DateField(primary_key=True)
    prompt = models.CharField(max_length=150, null=False)

    def __str__(self):
        return f"Prompt for {self.date}"
    
    
# JournalEntry table
class JournalEntry(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    entry = models.CharField(max_length=350, null=False)
    isReported = models.BooleanField(default=False)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True, blank=True)
    # stores the location of each entry
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name="liked_entries", blank=True)

    class Meta:
        unique_together = ('userID', 'date')  # Ensures each user can only have one entry per date
        verbose_name_plural = 'Entries'

    def __str__(self):
        return f"{self.userID.username} - {self.date}"


#Reported table
class Reported(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    entryID = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('userID', 'entryID')
        verbose_name_plural = 'Reported Entries'

    def __str__(self):
        return f"Report of entry {self.entryID} by {self.userID.username} on {self.date}"
