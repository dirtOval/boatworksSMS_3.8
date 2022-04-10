from django.db import models

# Create your models here.

#this is the class we're going to be texting initially.
class Parent(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    cell_phone = models.CharField(max_length=12, blank=True)
    home_phone = models.CharField(max_length=12, blank=True)
    work_phone = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=100, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    do_not_solicit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

#using this class to mark whether a student is graduated/in progress/dropped
class GraduationStatus(models.TextChoices):
    GRADUATED = "GR", "Graduated"
    DROPPED = "DR", "Dropped"
    IN_PROGRESS = "IP", "In Progress"

#this class holds the bulk of the data
class Student(models.Model):
    student_id = models.IntegerField(blank=True, null=True, default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grade_during_BKBW = models.CharField(max_length = 10, blank=True, default="")
    birthdate = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=100, blank=True)
    apartment = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    emergency_contact_name = models.CharField(max_length=50, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)
    graduation_status = models.CharField(
        max_length=2, choices=GraduationStatus.choices, default=GraduationStatus.GRADUATED
        )
    active_alum = models.CharField(max_length=30, blank=True)
    school = models.CharField(max_length=30, blank=True)
    year = models.CharField(max_length=4, blank=True, default="20XX")
    instructors = models.CharField(max_length=100, blank=True)
    media_consent = models.BooleanField(default=False, blank=True)
    program_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


#does this need more fields? I can't think of anything rn
class List(models.Model):
    name = models.CharField(max_length=100)
    parents = models.ManyToManyField(Parent, blank=True)

    def __str__(self):
        return self.name