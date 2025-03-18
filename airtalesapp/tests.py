from django.test import TestCase
from .models import User, JournalEntry

#testing user creation and authentication
class UserAuthentication(TestCase):
    def test_user_creation(self):
        user = User.objects.get_or_create_user(email="usertest1@example.com", username="usertest1", password="password123") #create test user
        self.assertEqual(user.email, "usertest1@example.com")#check email saved correctly
        self.assertEqual(user.username, "usertest1")#check username saved correctly
        self.assertTrue(user.check_password("password123"))#check password saved correctly and has been hashed

    def test_profile_creation(self):
        user = User.objects.get_or_create_user(email="test@example.com", username="testuser", password="password123")
        self.assertTrue(hasattr(user, 'profile'))#check profile has been created correctly


class JournalEntriesTest(TestCase):
    def setUp(self):#set up data for the tests
        self.user1 = User.objects.get_or_create_user(email="user1@example.com", username="user1", password="password123")
        self.user2 = User.objects.get_or_create_user(email="user2@example.com", username="user2", password="password123")
        
        self.entry = JournalEntry.objects.get_or_create(
            userID=self.user1, 
            date="2025-03-18", 
            defaults={"entry": "Test journal entry"}
        )[0]
    
    #test the likes are being implemented and counted correctly
    def test_likes(self):
        self.entry.liked_by.add(self.user2)
        self.assertEqual(self.entry.liked_by.count(), 1)
        self.assertTrue(self.user2 in self.entry.liked_by.all())
        self.entry.liked_by.remove(self.user2)
        self.assertEqual(self.entry.liked_by.count(), 0)
        self.assertFalse(self.user2 in self.entry.liked_by.all())

    #test that likes cannot go below zero
    def test_likes_cannot_go_below_zero(self):
        self.assertEqual(self.entry.liked_by.count(), 0)
     
        self.entry.liked_by.remove(self.user2)  
        
        self.assertGreaterEqual(self.entry.liked_by.count(), 0, "Likes should not be negative")

    #test that an entry can be reported correctly 
    def test_report_entry(self):
        self.entry.isReported = True
        self.entry.save()
        reported_entry = JournalEntry.objects.get(userID=self.user1, date="2025-03-18")
        self.assertTrue(reported_entry.isReported)

    #test that a user can only create one entry per date
    def test_unique_entry(self):
        with self.assertRaises(Exception):  
            JournalEntry.objects.create(
                userID=self.user1, 
                date="2025-03-18", 
                entry="This should fail"
            )
    
    #test that location data is being properly stored with the journal entry
    def test_location_data(self):
        self.entry.latitude = 37.7749
        self.entry.longitude = -122.4194
        self.entry.save()
        
        retrieved_entry = JournalEntry.objects.get(userID=self.user1, date="2025-03-18")
        self.assertEqual(retrieved_entry.latitude, 37.7749)
        self.assertEqual(retrieved_entry.longitude, -122.4194)
    
    #test that when a user is deleted their journal entries are deleted
    def test_user_deletion_cascade(self):
        entry2 = JournalEntry.objects.create(
            userID=self.user2, 
            date="2025-03-18", 
            entry="User2's entry"
        )
        
        user2_id = self.user2.userID
        self.user2.delete()
        
        with self.assertRaises(JournalEntry.DoesNotExist):
            JournalEntry.objects.get(userID=user2_id, date="2025-03-18")




