from django.urls import path
from . import views

app_name = "deals"

urlpatterns = [
    path('owner-details/solicitorListing/',views.solicitor_list,name='solicitorlisting'),
    path('owner-details/solicitorcreate/',views.solicitor_add,name='solicitor_create'),
    #
    path('owner-details/solicitorchangestatus/',views.solicitor_change_status,name='solicitor_change_status'),
    path('owner-details/agentchangestatus/',views.agent_change_status,name='agent_change_status'),
    path('owner-details/bankchangestatus/',views.bank_change_status,name='bank_change_status'),
    path('owner-details/familychangestatus/',views.family_change_status,name='family_change_status'),
    path('owner-details/executorchangestatus/',views.executor_change_status,name='executor_change_status'),
    path('owner-details/liquidatorchangestatus/',views.liquidator_change_status,name='liquidator_change_status'),
    path('owner-details/otherchangestatus/',views.other_change_status,name='other_change_status'),
    #
    path('owner-details/solicitorupdate/<pk>/',views.solicitor_edit,name='solicitor_edit'),
    path('owner-details/solicitordelete/<pk>/',views.solicitor_delete,name='solicitor_delete'),
    path('owner-details/agentListing/',views.agent_list,name='agentlisting'),
    path('owner-details/agentcreate/',views.agent_add,name='agent_create'),
    path('owner-details/agentupdate/<pk>/',views.agent_edit,name='agent_edit'),
    path('owner-details/agentdelete/<pk>/',views.agent_delete,name='agent_delete'),
    path('owner-details/bankListing/',views.bank_list,name='banklisting'),
    path('owner-details/bankcreate/',views.bank_add,name='bank_create'),
    path('owner-details/bankupdate/<pk>/',views.bank_edit,name='bank_edit'),
    path('owner-details/bankdelete/<pk>/',views.bank_delete,name='bank_delete'),
    path('owner-details/executorListing/',views.executor_list,name='executorlisting'),
    path('owner-details/executorcreate/',views.executor_add,name='executor_create'),
    path('owner-details/executorupdate/<pk>/',views.executor_edit,name='executor_edit'),
    path('owner-details/executordelete/<pk>/',views.executor_delete,name='executor_delete'),
    path('owner-details/familyListing/',views.family_list,name='familylisting'),
    path('owner-details/familycreate/',views.family_add,name='family_create'),
    path('owner-details/familyupdate/<pk>/',views.family_edit,name='family_edit'),
    path('owner-details/familydelete/<pk>/',views.family_delete,name='family_delete'),
    path('owner-details/liquidatorListing/',views.liquidator_list,name='liquidatorlisting'),
    path('owner-details/liquidatorcreate/',views.liquidator_add,name='liquidator_create'),
    path('owner-details/liquidatorupdate/<pk>/',views.liquidator_edit,name='liquidator_edit'),
    path('owner-details/liquidatordelete/<pk>/',views.liquidator_delete,name='liquidator_delete'),
    path('owner-details/otherListing/',views.other_list,name='otherlisting'),
    path('owner-details/othercreate/',views.other_add,name='other_create'),
    path('owner-details/otherupdate/<pk>/',views.other_edit,name='other_edit'),
    path('owner-details/otherdelete/<pk>/',views.other_delete,name='other_delete'),




    path('owner-details/solicitorList',views.SolicitorListView.as_view(),name='solicitorlist'),
    path('owner-details/solicitorCreate',views.SolicitorCreateView.as_view(),name='solicitorcreate'),
    path('owner-details/solicitorUpdate/<int:pk>/',views.SolicitorUpdateView.as_view(),name='solicitorupdate'),
    path('owner-details/solicitorDelete/<int:pk>/',views.SolicitorDeleteView.as_view(),name='solicitordelete'),
    path('owner-details/agentList',views.AgentListView.as_view(),name='agentlist'),
    path('owner-details/agentCreate',views.AgentCreateView.as_view(),name='agentcreate'),
    path('owner-details/agentUpdate/<int:pk>/',views.AgentUpdateView.as_view(),name='agentupdate'),
    path('owner-details/agentDelete/<int:pk>/',views.AgentDeleteView.as_view(),name='agentdelete'),
    path('owner-details/bankList',views.BankListView.as_view(),name='banklist'),
    path('owner-details/bankCreate',views.BankCreateView.as_view(),name='bankcreate'),
    path('owner-details/bankUpdate/<int:pk>/',views.BankUpdateView.as_view(),name='bankupdate'),
    path('owner-details/bankDelete/<int:pk>/',views.BankDeleteView.as_view(),name='bankdelete'),
    path('owner-details/executorList',views.ExecutorListView.as_view(),name='executorlist'),
    path('owner-details/executorCreate',views.ExecutorCreateView.as_view(),name='executorcreate'),
    path('owner-details/executorUpdate/<int:pk>/',views.ExecutorUpdateView.as_view(),name='executorupdate'),
    path('owner-details/executorDelete/<int:pk>/',views.ExecutorDeleteView.as_view(),name='executordelete'),
    path('owner-details/familyList',views.FamilyListView.as_view(),name='familylist'),
    path('owner-details/familyCreate',views.FamilyCreateView.as_view(),name='familycreate'),
    path('owner-details/familyUpdate/<int:pk>/',views.FamilyUpdateView.as_view(),name='familyupdate'),
    path('owner-details/familyDelete/<int:pk>/',views.FamilyDeleteView.as_view(),name='familydelete'),
    path('owner-details/liquidatorList',views.LiquidatorListView.as_view(),name='liquidatorlist'),
    path('owner-details/liquidatorCreate',views.LiquidatorCreateView.as_view(),name='liquidatorcreate'),
    path('owner-details/liquidatorUpdate/<int:pk>/',views.LiquidatorUpdateView.as_view(),name='liquidatorupdate'),
    path('owner-details/liquidatorDelete/<int:pk>/',views.LiquidatorDeleteView.as_view(),name='liquidatordelete'),
    path('owner-details/otherList',views.OtherListView.as_view(),name='otherlist'),
    path('owner-details/otherCreate',views.OtherCreateView.as_view(),name='othercreate'),
    path('owner-details/otherUpdate/<int:pk>/',views.OtherUpdateView.as_view(),name='otherupdate'),
    path('owner-details/otherDelete/<int:pk>/',views.OtherDeleteView.as_view(),name='otherdelete'),
    # path('owner-details/newview/',views.MyView.as_view(),name='newview'),
    path("deal/<int:lead_id>/", views.DealCardView.as_view(), name="deal"),
    path("dealsale/<int:lead_id>/", views.DealSaleCardView.as_view(), name="dealsale"),
    path(
        "<int:deal_id>/checklist/<slug:category>",
        views.CheckListView.as_view(),
        name="checklist",
    ),
    path(
        "owner-details/<int:deal_id>",
        views.OwnerDetailsView.as_view(),
        name="owner_details",
    ),
    path(
        "owner-details/edit/owner/<int:deal_id>",
        views.EditOwnerDetailsView.as_view(),
        name="edit_owner_details",
    ),
    path(
        "owner-details/edit/executor/<int:deal_id>",
        views.EditExecutorDetailsView.as_view(),
        name="edit_executor_details",
    ),
    path(
        "owner-details/edit/agent/<int:deal_id>",
        views.EditAgentDetailsView.as_view(),
        name="edit_agent_details",
    ),
    path(
        "owner-details/edit/solicitor/<int:deal_id>",
        views.EditSolicitorDetailsView.as_view(),
        name="edit_solicitor_details",
    ),
    path(
        "owner-details/edit/bank/<int:deal_id>",
        views.EditBankDetailsView.as_view(),
        name="edit_bank_details",
    ),
    path(
        "<int:deal_id>/inspection-details/land/",
        views.InspectionLandDetailsView.as_view(),
        name="inspection_details",
    ),
    path(
        "<int:deal_id>/inspection-details/land/selected-council/<str:contact_id>",
        views.InspectionLandDetailsSelectedCouncilView.as_view(),
        name="inspection_details_selected_council",
    ),
    path(
        "<int:deal_id>/inspection-details/external/",
        views.InspectionExternalDetailsView.as_view(),
        name="inspection_external_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/",
        views.GrannyFlatDetailsView.as_view(),
        name="inspection_granny_flat_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/entry/",
        views.EntryDetailsView.as_view(),
        name="inspection_entry_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/lounge/",
        views.LoungeDetailsView.as_view(),
        name="inspection_lounge_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/dining/",
        views.DiningDetailsView.as_view(),
        name="inspection_dining_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/kitchen/",
        views.KitchenDetailsView.as_view(),
        name="inspection_kitchen_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/laundry/",
        views.LaundryDetailsView.as_view(),
        name="inspection_laundry_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bathroom/",
        views.BathroomDetailsView.as_view(),
        name="inspection_bathroom_details",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bedroom/",
        views.BedroomDetailsView.as_view(),
        name="inspection_bedroom_details",
    ),
    path(
        "<int:deal_id>/loan-details/",
        views.LoanDetailsView.as_view(),
        name="loan_details",
    ),
    path(
        "<int:deal_id>/loan-details/afca-complaint-lodged",
        views.AFCAComplaintLodgedView.as_view(),
        name="afca_complaint_lodged",
    ),
    # Granny Flat Detail views
    path(
        "<int:deal_id>/inspection-details/granny-flat/entry",
        views.GrannyEntryDetailsView.as_view(),
        name="inspection_granny_flat_entry_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/lounge",
        views.GrannyLoungeDetailsView.as_view(),
        name="inspection_granny_flat_lounge_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/dining",
        views.GrannyDiningDetailsView.as_view(),
        name="inspection_granny_flat_dining_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/kitchen",
        views.GrannyKitchenDetailsView.as_view(),
        name="inspection_granny_flat_kitchen_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/laundry",
        views.GrannyLaundryDetailsView.as_view(),
        name="inspection_granny_flat_laundry_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/bathroom",
        views.GrannyBathroomDetailsView.as_view(),
        name="inspection_granny_flat_bathroom_details",
    ),
    path(
        "<int:deal_id>/inspection-details/granny-flat/bedroom",
        views.GrannyBedroomDetailsView.as_view(),
        name="inspection_granny_flat_bedroom_details",
    ),
    # Add and Delete Inspection details views
    path(
        "<int:deal_id>/inspection-details/internal/entry/add",
        views.AddEntryView.as_view(),
        name="inspection_entry_add",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/entry/delete",
        views.DeleteEntryView.as_view(),
        name="inspection_entry_delete",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/lounge/add",
        views.AddLoungeView.as_view(),
        name="inspection_lounge_add",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/lounge/delete",
        views.DeleteLoungeView.as_view(),
        name="inspection_lounge_delete",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/dining/add",
        views.AddDiningView.as_view(),
        name="inspection_dining_add",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/dining/delete",
        views.DeleteDiningView.as_view(),
        name="inspection_dining_delete",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bathroom/add",
        views.AddBathroomView.as_view(),
        name="inspection_bathroom_add",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bathroom/delete",
        views.DeleteBathroomView.as_view(),
        name="inspection_bathroom_delete",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bedroom/add",
        views.AddBedroomView.as_view(),
        name="inspection_bedroom_add",
    ),
    path(
        "<int:deal_id>/inspection-details/internal/bedroom/delete",
        views.DeleteBedroomView.as_view(),
        name="inspection_bedroom_delete",
    ),
    # Offer Details views
    path(
        "<int:deal_id>/offer-details/purchase",
        views.PurchaseDetailsView.as_view(),
        name="purchase_details",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/comparable-sales",
        views.PurchaseComparableSalesView.as_view(),
        name="purchase_comparable_sales",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/comparable-sales/add",
        views.AddPurchaseComparableSaleView.as_view(),
        name="add_purchase_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/comparable-sales/details/<int:comparable_sale_id>",
        views.PurchaseComparableSaleDetailsView.as_view(),
        name="purchase_comparable_sale_details",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/comparable-sales/edit/<int:comparable_sale_id>",
        views.EditPurchaseComparableSaleView.as_view(),
        name="edit_purchase_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/comparable-sales/del/",
        views.DelPurchaseComparableSaleView.as_view(),
        name="del_purchase_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/sale",
        views.SaleDetailsView.as_view(),
        name="sale_details",
    ),
    path(
        "<int:deal_id>/offer-details/sale/comparable-sales",
        views.SaleComparableSalesView.as_view(),
        name="sale_comparable_sales",
    ),
    path(
        "<int:deal_id>/offer-details/sale/comparable-sales/add",
        views.AddSaleComparableSaleView.as_view(),
        name="add_sale_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/sale/comparable-sales/details/<int:comparable_sale_id>",
        views.SaleComparableSaleDetailsView.as_view(),
        name="sale_comparable_sale_details",
    ),
    path(
        "<int:deal_id>/offer-details/sale/comparable-sales/edit/<int:comparable_sale_id>",
        views.EditSaleComparableSaleView.as_view(),
        name="edit_sale_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/sale/comparable-sales/del/",
        views.DelSaleComparableSaleView.as_view(),
        name="del_sale_comparable_sale",
    ),
    path(
        "<int:deal_id>/offer-details/purchase/feasibility-report",
        views.PurchaseFeasibilityReportView.as_view(),
        name="purchase_feasibility_report",
    ),
    # Renovation details views
    path(
        "<int:deal_id>/renovation-details",
        views.RenovationDetailsView.as_view(),
        name="renovation_details",
    ),
    path(
        "<int:deal_id>/renovation-team",
        views.RenovationTeamView.as_view(),
        name="renovation_team",
    ),
    path(
        "<int:deal_id>/renovation-team/add",
        views.AddRenovationTeamView.as_view(),
        name="renovation_team_add",
    ),
    path(
        "<int:deal_id>/renovation-team/fetch",
        views.FetchRenovationTeamView.as_view(),
        name="renovation_team_fetch_contact",
    ),
    path(
        "<int:deal_id>/renovation-team/delete",
        views.DeleteRenovationTeamView.as_view(),
        name="renovation_team_delete",
    ),
    path(
        "<int:deal_id>/renovation-details/confirm",
        views.ConfirmRenovationTeamView.as_view(),
        name="renovation_team_confirm",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms",
        views.RenovationRoomsView.as_view(),
        name="renovation_rooms",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/overview",
        views.RenovationRoomsDetailsView.as_view(),
        name="renovation_rooms_details",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/tasks",
        views.RenovationRoomsTasksView.as_view(),
        name="renovation_rooms_tasks_details",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/materials",
        views.RenovationRoomsMaterialsView.as_view(),
        name="renovation_rooms_materials_details",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/overview/select-details",
        views.RenovationRoomsSelectDetailsView.as_view(),
        name="renovation_rooms_select_details",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/tasks/select-details",
        views.RenovationRoomsTasksSelectDetailsView.as_view(),
        name="renovation_rooms_tasks_select_details",
    ),
    path(
        "<int:deal_id>/renovation-details/rooms/<int:room_id>/materials/select-details",
        views.RenovationRoomsMaterialsSelectDetailsView.as_view(),
        name="renovation_rooms_materials_select_details",
    ),
    path(
        "<int:deal_id>/renovation-details/add-or-edit-images/<slug:category>",
        views.AddOrEditRenovationImagesView.as_view(),
        name="renovation_images_add_or_edit",
    ),
    path(
        "<int:deal_id>/renovation-details/images",
        views.RenovationImagesView.as_view(),
        name="renovation_images",
    ),
    path(
        "render-renovation-image-form/<int:form_id>",
        views.RenderRenovationImageFormView.as_view(),
        name="renovation_images_form_view",
    ),
    path(
        "<int:deal_id>/renovation-details/external",
        views.RenovationExternalView.as_view(),
        name="renovation_external",
    ),
    path(
        "<int:deal_id>/renovation/add-or-edit-external-location",
        views.AddOrEditExternalLocationsView.as_view(),
        name="add_or_edit_external_locations",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/overview",
        views.RenovationExternalLocationDetailsView.as_view(),
        name="renovation_external_location_details",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/tasks",
        views.RenovationExternalLocationTasksView.as_view(),
        name="renovation_external_location_tasks_details",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/materials",
        views.RenovationExternalLocationMaterialsView.as_view(),
        name="renovation_external_location_materials_details",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/overview/select-details",
        views.RenovationExternalLocationSelectDetailsView.as_view(),
        name="renovation_locations_select_details",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/tasks/select-details",
        views.RenovationExternalLocationTasksSelectDetailsView.as_view(),
        name="renovation_external_location_tasks_select_details",
    ),
    path(
        "<int:deal_id>/renovation-details/external/<int:location_id>/materials/select-details",
        views.RenovationExternalLocationMaterialsSelectDetailsView.as_view(),
        name="renovation_external_location_materials_select_details",
    ),
    # My purchase details url
    path(
        "<int:deal_id>/my-purchase-details",
        views.MyPurchaseDetailsView.as_view(),
        name="my_purchase_details",
    ),
    path(
        "<int:deal_id>/my-purchase-details/edit-lender/<int:lender_id>",
        views.EditLenderDetailsView.as_view(),
        name="edit_lender_details",
    ),
    path(
        "<int:deal_id>/my-purchase-details/remove-lender/<int:lender_id>",
        views.RemoveLenderDetailsView.as_view(),
        name="remove_lender_details",
    ),
    path(
        "<int:deal_id>/render-my-details/lender/<int:lender_id>",
        views.RenderLenderDetailsView.as_view(),
        name="render_lender_details",
    ),
    path(
        "<int:deal_id>/render-my-details/contact/<int:contact_id>",
        views.RenderContactDetailsView.as_view(),
        name="render_contact_details",
    ),
    path(
        "<int:deal_id>/render-my-details/entity/<int:entity_id>",
        views.RenderEntityDetailsView.as_view(),
        name="render_entity_details",
    ),
    path(
        "<int:deal_id>/add-or-edit-bank",
        views.AddOrEditBankView.as_view(),
        name="add_or_edit_bank_details",
    ),
    path(
        "<int:deal_id>/purchase-correspondance-documents",
        views.PurchaseCorrespondanceDocumentsView.as_view(),
        name="purchase_correspondance_documents",
    ),
    path(
        "<int:deal_id>/add-or-edit-purchase-correspondance-documents",
        views.AddOrEditPurchaseCorrespondanceDocumentView.as_view(),
        name="add_or_edit_purchase_correspondance_documents",
    ),
    path(
        "render-purchase-document-form/<int:form_id>",
        views.RenderPurchaseDocumentFormView.as_view(),
        name="purchase_document_form_view",
    ),
    path(
        "<int:deal_id>/download-purchase-correspondance-document/<int:document_id>",
        views.DownloadPurchaseCorrespondanceDocument.as_view(),
        name="download_purchase_correspondance_document",
    ),
    path(
        "<int:deal_id>/reminders-list",
        views.RemindersListView.as_view(),
        name="reminders_list",
    ),
    path(
        "<int:deal_id>/add-reminder",
        views.AddReminderView.as_view(),
        name="add_reminder",
    ),
    path(
        "<int:deal_id>/edit-reminder/<int:reminder_id>",
        views.EditReminderView.as_view(),
        name="edit_reminder",
    ),
    path(
        "<int:deal_id>/delete-reminder/<int:reminder_id>",
        views.DeleteReminderView.as_view(),
        name="delete_reminder",
    ),
    # List For Sale
    path(
        "<int:deal_id>/list-for-sale",
        views.ListForSaleView.as_view(),
        name="list_for_sale",
    ),
    path("<int:deal_id>/sold", views.SoldView.as_view(), name="sold"),
]
