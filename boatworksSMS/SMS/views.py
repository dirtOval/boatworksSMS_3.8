from multiprocessing import context
from unicodedata import name
from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from SMS.utils import fetch_sms
from .models import Parent, Student, List
from .forms import ParentCreateForm, StudentCreateForm, ListCreateForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db.models import Q
from twilio.base.exceptions import TwilioRestException

# Create your views here.

#Authentication Views
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def home_view(request):
    return render(request, "SMS/home_view.html")

class NewUserView(LoginRequiredMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/newusercreate.html"

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template = "SMS/userlist.html"

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = "auth/userupdateview.html"
    success_message = "User Updated!"
    success_url = reverse_lazy("userlist")


#Messaging Views
@login_required
def messaging_view(request):
    lists = List.objects.all()
    context = {"lists": lists}
    return render(request, "SMS/messaging_view.html", context)

@login_required
def send_view(request):
    #here i need to: 1. grab numbers from people in list. 2. convert numbers to proper format
    message_to_broadcast = request.GET.get("msg")
    list_selected = request.GET.get("list_selection")
    list_filtered = List.objects.get(pk=list_selected)
    numbers = []
    for person in list_filtered.parents.all():
        numbers.append(person.cell_phone)
    #to format numbers split by "-", add +1, form together
    numbers_formatted = []
    for number in numbers:
        parts = number.split("-")
        reassembled = "".join(parts)
        finished = "+1" + reassembled

        numbers_formatted.append(finished)

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #this is for accumulating the numbers that throw TwilioRestException
    failed_numbers = []
    for recipient in numbers_formatted:
        try:
            if recipient:
                client.messages.create(to=recipient,
                                    from_=settings.TWILIO_NUMBER,
                                    body=message_to_broadcast)
        except TwilioRestException:
            failed_numbers.append(recipient)
            continue
    context = {"numbers": numbers_formatted, "failed": failed_numbers}
    return render(request, "SMS/send_view.html", context)

@login_required
def message_log_view(request):
    sms = fetch_sms()
    log = [x for x in sms]
    context = {"log": log}
    return render(request, "SMS/message_log_view.html", context)

#Address Book Views
@login_required
def address_book_view(request):
    return render(request, "SMS/address_book_view.html")


class ParentListView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = "SMS/parentlistview.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParentListView, self).get_context_data(*args, **kwargs)
        context['lists'] = List.objects.all()
        return context

class ParentSearchResultListView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = "SMS/parentsearchresultlistview.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParentSearchResultListView, self).get_context_data(*args, **kwargs)
        context['lists'] = List.objects.all()
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Parent.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(cell_phone__icontains=query) |
            Q(home_phone__icontains=query) |
            Q(work_phone__icontains=query) |
            Q(email__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__first_name__icontains=query) )

@login_required
def parent_field_search_view(request):
    return render(request, "SMS/parent_field_search_view.html")

class ParentFieldSearchResultListView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = "SMS/parentfieldsearchresultlistview.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParentFieldSearchResultListView, self).get_context_data(*args, **kwargs)
        context['lists'] = List.objects.all()
        return context

    def get_queryset(self):
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        grade_during_BKBW = self.request.GET.get("grade_during_BKBW")
        birthdate = self.request.GET.get("birthdate")
        email = self.request.GET.get("email")
        phone = self.request.GET.get("phone")
        address = self.request.GET.get("address")
        apartment = self.request.GET.get("apartment")
        city = self.request.GET.get("city")
        state = self.request.GET.get("state")
        zip_code = self.request.GET.get("zip_code")
        emergency_contact_name = self.request.GET.get("emergency_contact_name")
        emergency_contact_relationship = self.request.GET.get("emergency_contact_relationship")
        emergency_contact_phone = self.request.GET.get("emergency_contact_phone")
        graduation_status = self.request.GET.get("graduation_status")
        active_alum = self.request.GET.get("active_alum")
        school = self.request.GET.get("school")
        year = self.request.GET.get("year")
        instructors = self.request.GET.get("instructors")
        media_consent = self.request.GET.get("media_consent")
        program_type = self.request.GET.get("program_type")
        field_list = {"first_name__icontains": first_name,
                      "last_name__icontains": last_name,
                      "grade_during_BKBW__icontains": grade_during_BKBW,
                      "birthdate__icontains": birthdate,
                      "email__icontains": email,
                      "phone__icontains": phone,
                      "address__icontains": address,
                      "apartment__icontains": apartment,
                      "city__icontains": city,
                      "state__icontains": state,
                      "zip_code__icontains": zip_code,
                      "emergency_contact_name__icontains": emergency_contact_name,
                      "emergency_contact_relationship__icontains": emergency_contact_relationship,
                      "emergency_contact_phone__icontains": emergency_contact_phone,
                      "graduation_status__icontains": graduation_status,
                      "active_alum__icontains": active_alum,
                      "school__icontains": school,
                      "year__icontains": year,
                      "instructors__icontains": instructors,
                      "media_consent__icontains": media_consent,
                      "program_type__icontains": program_type}
        student_list = Student.objects.all()
        for field in field_list:
            if field_list[field]:
                student_list = student_list.filter(**{field: field_list[field]})
        #so we have the filtered list of students, now to get their parents
        parent_list = Parent.objects.filter(student__in=student_list)
        return parent_list

@login_required
def parent_list_add_view(request):
    parents_selected = request.POST.getlist("parent")
    list_selected = request.POST.get("list_selection")
    list_filtered = List.objects.get(pk=list_selected)
    parents_added = []
    for parent in parents_selected:
        list_filtered.parents.add(parent)
        parents_added.append(Parent.objects.get(pk=parent))
    context = {"parents_added": parents_added}
    return render(request, "SMS/parent_list_add_view.html", context)

class ParentCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    form_class = ParentCreateForm
    template_name = "SMS/parentcreateview.html"
    success_message = "Parent Added!"
    success_url = reverse_lazy("parentlist")

class ParentUpdateView(LoginRequiredMixin, UpdateView):
    model = Parent
    form_class = ParentCreateForm
    template_name = "SMS/parentupdateview.html"
    success_message = "Parent Updated!"
    success_url = reverse_lazy("parentlist")

class ParentDeleteView(LoginRequiredMixin, DeleteView):
    model = Parent
    template_name = "SMS/parentdeleteview.html"
    success_message = "Parent Deleted!"
    success_url = reverse_lazy("parentlist")

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "SMS/studentlistview.html"

class StudentSearchResultListView(LoginRequiredMixin, ListView):
    model = Student
    template_name ="SMS/studentsearchresultlistview.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(grade_during_BKBW__icontains=query) |
            Q(birthdate__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(address__icontains=query) |
            Q(apartment__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(zip_code__icontains=query) |
            Q(emergency_contact_name__icontains=query) |
            Q(emergency_contact_relationship__icontains=query) |
            Q(emergency_contact_phone__icontains=query) |
            Q(graduation_status__icontains=query) |
            Q(active_alum__icontains=query) |
            Q(school__icontains=query) |
            Q(year__icontains=query) |
            Q(instructors__icontains=query) |
            Q(program_type__icontains=query))


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "SMS/studentcreateview.html"
    success_message = "Student created!"
    success_url = reverse_lazy("studentlist")

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "SMS/studentupdateview.html"
    success_message = "Student Updated!"
    success_url = reverse_lazy("studentlist")

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "SMS/studentdeleteview.html"
    success_message = "Student Deleted!"
    success_url = reverse_lazy("studentlist")

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "SMS/listlistview.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "SMS/listdetailview.html"

@login_required
def list_detail_remove_view(request, pk):
    list_id = pk
    parents_to_remove = request.POST.getlist("parents")
    list = List.objects.get(pk=list_id)
    parents_removed = []
    for parent in parents_to_remove:
        list.parents.remove(parent)
        parents_removed.append(Parent.objects.get(pk=parent))

    return render(request, "SMS/list_detail_remove_view.html", context={"parents_removed": parents_removed})

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    form_class = ListCreateForm
    template_name = "SMS/listcreateview.html"
    success_message = "List created!"
    success_url = reverse_lazy("listlist")

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    form_class = ListCreateForm
    template_name = "SMS/listupdateview.html"
    success_message = "List Updated!"
    success_url = reverse_lazy("listlist")

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "SMS/listdeleteview.html"
    success_message = "List Deleted!"
    success_url = reverse_lazy("listlist")