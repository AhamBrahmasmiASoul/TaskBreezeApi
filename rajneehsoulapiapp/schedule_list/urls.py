from django.urls import path

from rajneehsoulapiapp.schedule_list.views import ScheduleItemView, UploadScheduleAttachmentsView

urlpatterns = [
    path('schedule-items', ScheduleItemView.as_view()),
    path('schedule-items/<int:item_id>', ScheduleItemView.as_view()),
    path('schedule-items/upload-attachments', UploadScheduleAttachmentsView.as_view(), name='upload-attachments'),
]