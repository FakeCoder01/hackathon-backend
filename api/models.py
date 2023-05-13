from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.hashers import check_password, make_password
# Create your models here.

class Office(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    office_location = models.CharField(max_length=40)
    def __str__(self) -> str:
        return self.office_location

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    department_name = models.CharField(max_length=40)
    
    def __str__(self) -> str:
        return self.department_name

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    department_id = models.ForeignKey(Department, related_name="positions", on_delete=models.CASCADE)
    position_name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.position_name


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, related_name="userprofile", editable=False, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=8)
    age = models.PositiveIntegerField()

    department = models.ForeignKey(Department, related_name="departmentuser", on_delete=models.CASCADE)
    position = models.ForeignKey(Position, related_name="positionuser", on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="useroffice")
    
    description = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name


class Social(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="socails")
    name = models.CharField(max_length=100) # FB, Insta, VK ..
    url = models.URLField()

    def __str__(self) -> str:
        return str(self.name)
    
    def get_social(self):
        return {
            "account" : self.name,
            "link" : str(self.url)
        }

class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="photos/", default="photos/user.jpg")
    def __str__(self) -> str:
        return str(self.photo)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=40)
    role = models.CharField(max_length=100)
    joined = models.DateField()
    left = models.DateField()

    details = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.role + " " + self.company)
    
class Account(models.Model):
    user = models.OneToOneField(User, related_name="useraccount", editable=False, on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.TextField(null=True, blank=True)
    sent_on = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email
    
    def set_otp(self, otp):
        try:
            otp = str(otp)
            self.otp = make_password(otp)
            return True
        except Exception as err:
            print(err)
            return False
        
    def verify_otp(self, hash):
        if check_password(hash, self.otp):
            self.status = True
        self.save()
        return self.status