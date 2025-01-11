from django.urls import path
from .views import GroupExpenseView, CollaboratorDetailView, ExpenseItemView

urlpatterns = [
    # GroupExpenseView routes
    path('group-expense', GroupExpenseView.as_view(), name='group-expense-list'),
    path('group-expense/<int:group_id>', GroupExpenseView.as_view(), name='group-expense-detail'),

    # CollaboratorDetailView routes
    path('collaborator', CollaboratorDetailView.as_view(), name='collaborator-list'),
    path('collaborator/<int:collaborator_id>', CollaboratorDetailView.as_view(), name='collaborator-detail'),

    # ExpenseItemView routes
    path('expense', ExpenseItemView.as_view(), name='expense-list'),
    path('expense/<int:expense_id>', ExpenseItemView.as_view(), name='expense-detail'),
]
