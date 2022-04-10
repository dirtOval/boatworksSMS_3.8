from django import forms
from .models import Parent, Student, List
from django.core.exceptions import ValidationError

class ParentCreateForm(forms.ModelForm):
    
    #this is so the student list is alphabetized
    student = forms.ModelChoiceField(queryset=Student.objects.order_by('last_name'))

    def clean_cell_phone(self):
        number = self.cleaned_data['cell_phone']
        chars = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()_=+,<.>/?`~[{]}\|:;'"
        only_numbers = True
        for char in chars:
            if char in number:
                only_numbers = False
        if number:
            if len(number) < 12:
                raise ValidationError("Numbers must be exactly 12 characters!")
            if number[3] != "-" or number[7] != "-":
                raise ValidationError("Numbers must be entered in xxx-xxx-xxxx format!")
            if only_numbers == False:
                raise ValidationError("Numbers may not contain letters or special characters!")
        return number

    class Meta:
        model = Parent
        fields = ('first_name', 'last_name', 'cell_phone', 'home_phone', 'work_phone', 'email', 'student', 'do_not_solicit')

class StudentCreateForm(forms.ModelForm):

    def clean_phone(self):
        number = self.cleaned_data['phone']
        chars = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()_=+,<.>/?`~[{]}\|:;'"
        only_numbers = True
        for char in chars:
            if char in number:
                only_numbers = False
        if number:
            if len(number) < 12:
                    raise ValidationError("Numbers must be exactly 12 characters!")
            if number[3] != "-" or number[7] != "-":
                raise ValidationError("Numbers must be entered in xxx-xxx-xxxx format!")
            if only_numbers == False:
                raise ValidationError("Numbers may not contain letters or special characters!")
        return number

    class Meta:
        model = Student
        exclude =  ['student_id']

class ListCreateForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ('name',)