from celery.result import AsyncResult
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView, DeleteView
)
from django.views.generic.base import View

from schemas.forms import ColumnForm, DataSetCreateForm
from schemas.models import Schema, Column_m, DataSet
from .tasks import form_fake_data


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'schema/schema_list.html'


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    template_name = 'schema/schema_create.html'
    fields = ['title']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(SchemaCreateView, self).form_valid(form)
        return valid_data


class SchemaDetailView(LoginRequiredMixin,DetailView):
    model = Schema
    template_name = 'schema/schema_detail.html'


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy('list')
    template_name = 'schema/schema_delete.html'


class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column_m
    form_class = ColumnForm
    template_name = 'schema/column_create.html'

    def form_valid(self, form):
        schema = Schema.objects.get(pk=self.kwargs["pk"])
        form.instance.schema = schema
        return super().form_valid(form)


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column_m
    template_name = 'schema/column_delete.html'

    def get_success_url(self, **kwargs):
        column = Column_m.objects.get(pk=self.kwargs["pk"])
        schema = Schema.objects.get(column_m=column)
        return reverse_lazy('detail', kwargs={'pk': schema.pk})


# class DataList(ListView):
#     model = DataSet
#     template_name = 'schema/schema_dataset.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['schema'] = Schema.objects.get(pk=self.kwargs["pk"])
#         return context
#
#
# class DataCreateView(LoginRequiredMixin, CreateView):
#     model = DataSet
#     form_class = DataSetCreateForm
#     template_name = 'schema/dataset_create.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['schema'] = Schema.objects.get(pk=self.kwargs["pk"])
#         return context
#
#     def form_valid(self, form):
#         schema = Schema.objects.get(pk=self.kwargs["pk"])
#         if schema:
#             form.instance.schema = schema
#             valid = super().form_valid(form)
#             form_fake_data.delay(schema.id, form.instance.id)
#             return valid
#         else:
#             form.add_error('order', 'Error')

class SchemaView(LoginRequiredMixin, View):
    """
    Responsible for schema detail and related datasets page.
    Display datasets table and create dataset form.
    Receive a POST AJAX request, create new dataset model,
    start Celery task to form CSV file and send json data to front end.
    """
    def get(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id, user=request.user)
        data_sets = schema.dataset_set.all()
        form = DataSetCreateForm()
        context = {'schema': schema, 'data_sets': data_sets, 'form': form}
        return render(request, 'schema/schema_dataset.html', context)

    def post(self, request, schema_id):
        if request.is_ajax():
            schema = Schema.objects.get(id=schema_id, user=request.user)
            form = DataSetCreateForm(data=request.POST)

            if form.is_valid():
                data_set = DataSet.objects.create(
                    schema_id=schema_id,
                    num_row=request.POST.get('num_row')
                )
                task = form_fake_data.delay(
                    schema_id, data_set.num_row, data_set.id
                )

                response = {
                    'task_id': task.id,
                    'count': schema.dataset_set.count(),
                    'dataset_id': data_set.id,
                    'created': data_set.created,
                    'status': data_set.status
                }

                return JsonResponse(response, status=202)

        else:
            return HttpResponseForbidden(status=403)


class TaskStatusView(LoginRequiredMixin, View):
    """
    Realize Celery task status polling.
    Recieve a GET AJAX request, check task status and send json data to front end.
    """
    def get(self, request, task_id):
        if request.is_ajax():
            task_result = AsyncResult(task_id)
            result = {
                "task_id": task_id,
                "task_status": task_result.status
            }
            return JsonResponse(result, status=202)

        else:
            return HttpResponseForbidden(status=403)


class FileDownloadView(LoginRequiredMixin, View):

    def get(self, request, dataset_id):
        data_set = get_object_or_404(DataSet, id=dataset_id)
        print(data_set.file)
        return FileResponse(open(str(data_set.file), 'rb'))
