from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("users", views.UserListView.as_view(), name="userlist"),
    path("users/<pk>/update", views.UserUpdateView.as_view(), name="userupdate"),
    path("users/create", views.NewUserView.as_view(), name="newuser"),
    path("", views.home_view, name="home"),
    path("messaging", views.messaging_view, name="messaging"),
    path("messaging/send", views.send_view, name="send"),
    path("messaging/messagelog", views.message_log_view, name="messagelog"),
    path("addressbook", views.address_book_view, name="addressbook"),
    path("addressbook/parents", views.ParentListView.as_view(), name="parentlist"),
    path("addressbook/parents/search", views.ParentSearchResultListView.as_view(), name="parentsearch"),
    path("addressbook/parents/filter", views.parent_field_search_view, name="filter"),
    path("addressbook/parents/filtersearch", views.ParentFieldSearchResultListView.as_view(), name="filtersearch"),
    path("addressbook/parents/create", views.ParentCreateView.as_view(), name="parentcreate"),
    path("addressbook/parents/<pk>/update", views.ParentUpdateView.as_view(), name="parentupdate"),
    path("addressbook/parents/<pk>/delete", views.ParentDeleteView.as_view(), name="parentdelete"),
    path("addressbook/parents/listadd", views.parent_list_add_view, name="listadd"),
    path("addressbook/students", views.StudentListView.as_view(), name="studentlist"),
    path("addressbook/students/search", views.StudentSearchResultListView.as_view(), name="studentsearch"),
    path("addressbook/students/create", views.StudentCreateView.as_view(), name="studentcreate"),
    path("addressbook/students/<pk>/update", views.StudentUpdateView.as_view(), name="studentupdate"),
    path("addressbook/students/<pk>/delete", views.StudentDeleteView.as_view(), name="studentdelete"),
    path("addressbook/lists", views.ListListView.as_view(), name="listlist"),
    path("addressbook/lists/<pk>/detail", views.ListDetailView.as_view(), name="listdetail"),
    path("addressbook/lists/<pk>/detail/remove", views.list_detail_remove_view, name="listdetailremove"),
    path("addressbook/lists/create", views.ListCreateView.as_view(), name="listcreate"),
    path("addressbook/lists/<pk>/update", views.ListUpdateView.as_view(), name="listupdate"),
    path("addressbook/lists/<pk>/delete", views.ListDeleteView.as_view(), name="listdelete")

]