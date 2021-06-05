from django.urls import path

from .views import *

urlpatterns = [
    path('', SchemaListView.as_view(), name='list'),
    path('new/', SchemaCreateView.as_view(), name='create'),
    path('<int:pk>/detail/', SchemaDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', SchemaDeleteView.as_view(), name='delete'),
    path('<int:pk>/add/', ColumnCreateView.as_view(), name='column-create'),
    path('<int:pk>/column_delete/', ColumnDeleteView.as_view(),
         name='column_delete'),
#     path('schema/get_file/<int:dataset_id>/', FileDownloadView.as_view(),
#          name='get_file'),
    path('schema/<int:schema_id>/', SchemaView.as_view(), name='data-set'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task_status')
#     path('<int:pk>/data/', DataList.as_view(), name="data-set"),
#     path('<int:pk>/data/add/', DataCreateView.as_view(), name="data-add"),
]
