from django.db import models

# Create your models here.
class BookTest(models.Model):
    TEST_CHOICES = [
        ('IELTS Academic', 'IELTS Academic'),
        ('IELTS CBT', 'IELTS CBT'), 
        ('IELTS UKVI', 'IELTS UKVI'),
        ('IELTS General', 'IELTS General'),
        ('PTE Academic', 'PTE Academic'),
        ('PTE Academic UKVI', 'PTE Academic UKVI'),
        ('PTE Core', 'PTE Core'),
        ('OET', 'OET'),
        ('Duolingo Test', 'Duolingo Test'),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    preferred_date = models.DateField()
    test_type = models.CharField(choices=TEST_CHOICES, max_length=50)
    test_mode = models.CharField(max_length=50)
    confirmation_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.test_type} on {self.preferred_date}"
    
class CallbackRequest(models.Model):
    full_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} - {self.contact_number}"

class CounsellingAppointment(models.Model):
    DESTINATION_CHOICES = [
        ('USA', 'USA'),
        ('Canada', 'Canada'),
        ('UK', 'UK'),
        ('Australia', 'Australia'),
        ('New Zealand', 'New Zealand'),
        ('Germany', 'Germany'),
        ('France', 'France'),
        ('Other', 'Other'),
    ]
    ACADEMIC_LEVEL_CHOICES = [
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('PhD', 'PhD'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
    ]
    CURRENT_ACADEMIC_LEVEL_CHOICES = [
        ('High School', 'High School'),
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('PhD', 'PhD'),
        ('Other', 'Other'),
    ]
    MODE_CHOICES = [
        ('In-Person', 'In-Person'),
        ('Online', 'Online'),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    preferred_destination = models.CharField(choices=DESTINATION_CHOICES, max_length=50)
    intended_academic_level = models.CharField(choices=ACADEMIC_LEVEL_CHOICES, max_length=50)
    current_academic_level = models.CharField(choices=CURRENT_ACADEMIC_LEVEL_CHOICES, max_length=50)
    counselling_mode = models.CharField(choices=MODE_CHOICES, max_length=20)
    accept_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date} at {self.preferred_time}"