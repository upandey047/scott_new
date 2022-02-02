from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("<slug:contacts_category>/<slug:contacts_sub_category>",views.ContactsView.as_view(), name="index",),
    path("<slug:contacts_category>/<slug:contacts_sub_category>/edit/<int:contact_id>",views.EditContactView.as_view(),name="edit",),
    path("<int:contact_id>", views.DeleteContactView.as_view(), name="delete"),
    path("add/<slug:contacts_category>/<slug:contacts_sub_category>",views.AddContactView.as_view(),name="add",),
]
