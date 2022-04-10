from django.contrib import admin
from .models import List, Student, Parent
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

admin.site.register(List)

#this is stuff for import_export
class StudentResource(resources.ModelResource):

    class Meta:
        model = Student

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('student_id', 'first_name', 'last_name', 'grade_during_BKBW', 'birthdate', 'email', 'phone', 'address', 'apartment', 'city', 'state', 'zip_code', 'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone', 'graduation_status', 'active_alum', 'school', 'year', 'instructors', 'media_consent', 'program_type')

admin.site.register(Student, StudentAdmin)

class ParentResource(resources.ModelResource):
    student = fields.Field(attribute="student", column_name="student_id", widget=ForeignKeyWidget(Student, 'student_id'))
    class Meta:
        model = Parent

class ParentAdmin(ImportExportModelAdmin):
    resource_class = ParentResource
    list_display = ('student', 'first_name', 'last_name', 'cell_phone', 'home_phone', 'work_phone', 'email', 'do_not_solicit')

admin.site.register(Parent, ParentAdmin)