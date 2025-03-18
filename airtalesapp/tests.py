from django.test import TestCase
from django.utils.timezone import now
from .models import User, JournalEntry

class JournalEntriesMethodTest(TestCase):
    def setUp(self):
        # Don't try to unpack the return value
        self.user1 = User.objects.get_or_create_user(email="user1@example.com", username="user1", password="password123")
        self.user2 = User.objects.get_or_create_user(email="user2@example.com", username="user2", password="password123")
        
        # For JournalEntry, use get_or_create properly (it returns a tuple)
        self.entry, _ = JournalEntry.objects.get_or_create(
            userID=self.user1, 
            date="2025-03-18", 
            defaults={"entry": "Test journal entry"}
        )
    
    def test_likes_cannot_go_below_zero(self):
        self.assertEqual(self.entry.liked_by.count(), 0)
     
        self.entry.liked_by.remove(self.user2)  
        
        self.assertGreaterEqual(self.entry.liked_by.count(), 0, "Likes should not be negative")


#testing user creation and authentication
class UserAuthentication(TestCase):
    def user_creation(self):
        user = User.objects.get_or_create_user(email="usertest1@example.com", username="usertest1", password="password123") #create test user
        self.assertEqual(user.email, "usertest1@example.com")#check email saved correctly
        self.assertEqual(user.username, "usertest1")#check username saved correctly
        self.assertTrue(user.check_password("password123"))#check password saved correctly

    def test_profile_creation(self):
        user = User.objects.get_or_create_user(email="test@example.com", username="testuser", password="password123")
        self.assertTrue(hasattr(user, 'profile'))
    
