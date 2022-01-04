from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path(
        "individual",
        views.IndividualEntityView.as_view(),
        name="individual_entity",
    ),
    path("company", views.CompanyEntityView.as_view(), name="company_entity"),
    path("trust", views.TrustEntityView.as_view(), name="trust_entity"),
    path(
        "individual/edit/<int:pk>",
        views.EditIndividualEntityView.as_view(),
        name="edit_individual_entity",
    ),
    path(
        "company/edit/<int:pk>",
        views.EditCompanyEntityView.as_view(),
        name="edit_company_entity",
    ),
    path(
        "trust/edit/<int:pk>",
        views.EditTrustEntityView.as_view(),
        name="edit_trust_entity",
    ),
    path(
        "individual/add",
        views.IndividualEntityView.as_view(),
        name="add_individual_entity",
    ),
    path(
        "company/add",
        views.CompanyEntityView.as_view(),
        name="add_company_entity",
    ),
    path(
        "trust/add", views.TrustEntityView.as_view(), name="add_trust_entity"
    ),
    path(
        "checklist/<slug:checklist_category>",
        views.CheckListView.as_view(),
        name="checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/add",
        views.AddEventToCheckListView.as_view(),
        name="add_event_to_checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/edit/<int:pk>",
        views.EditEventOfCheckListView.as_view(),
        name="edit_event_of_checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/delete/<int:pk>",
        views.DeleteEventOfCheckListView.as_view(),
        name="delete_event_of_checklist",
    ),
]
