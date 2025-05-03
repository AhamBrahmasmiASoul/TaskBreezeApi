from django.urls import path
from .views import GroupAPIView, CollaboratorAPIView, ExpenseAPIView

urlpatterns = [
    path('groups', GroupAPIView.as_view(), name='group-api'),
    path('collaborators', CollaboratorAPIView.as_view(), name='collaborator-api'),
    path('expenses', ExpenseAPIView.as_view(), name='expense_api'),
    path('expenses/<int:expense_id>', ExpenseAPIView.as_view(), name='expense_detail_api'),
]
