from django.db import models

class PhoneNumber(models.Model):
    countryCode = models.CharField(max_length=10)
    number = models.CharField(max_length=15)

class Career(models.Model):
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    linkedIn = models.URLField()
    currentLocation = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    jobType = models.CharField(max_length=50)

class Contact(models.Model):
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    projectName = models.CharField(max_length=100)
    services = models.CharField(max_length=100)
    message = models.TextField()

class BookDemo(models.Model):
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    companyName = models.CharField(max_length=100)
    jobTitle = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    members = models.CharField(max_length=20)

class Submission(models.Model):
    career = models.OneToOneField(Career, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    bookDemo = models.OneToOneField(BookDemo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
