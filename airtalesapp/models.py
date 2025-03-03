from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

# # User manager
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
             password=password,
         )
        # user.set_password(password) # hashes the password before saving
         user.save(using=self._db)
         return user

     def create_superuser(self, email, username, password):
         user = self.create_user(email, username, password)
         user.is_admin = True
         user.save(using=self._db)
         return user

 # User table
#class User(AbstractBaseUser, PermissionsMixin):
class User(AbstractBaseUser, PermissionsMixin):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    # password = models.CharField(max_length=30, default=make_password("defaultpassword")) 
    password = models.CharField(max_length=128) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Needed for admin panel access
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )
    # def save(self, *args, **kwargs):
    #     """Ensure password is hashed before saving."""
    #     if not self.password.startswith('pbkdf2_'):
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

 # JournalEntry table
class JournalEntry(models.Model):
     userID = models.ForeignKey(User, on_delete=models.CASCADE)
     date = models.DateField(default=now)
     entry_text = models.TextField(max_length=350, null=False)
     created_at = models.DateTimeField(default=now)
     isReported = models.BooleanField(default=False)

     class Meta:
         unique_together = ('userID', 'date')  # Ensures each user can only have one entry per date

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
#class Reported(models.Model):
#     UserID = models.ForeignKey(User, on_delete=models.CASCADE)
#     Date = models.DateField()
#     IsReported = models.ForeignKey(JournalEntry, to_field="IsReported", on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('UserID', 'Date')

     #def __str__(self):
       # return f"Report - {self.UserID.Username} on {self.Date}"