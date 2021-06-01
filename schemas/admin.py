from django.contrib import admin

from schemas.models import Type, Schema, Column_m, DataSet

admin.site.register(Type)
admin.site.register(Schema)
admin.site.register(Column_m)
admin.site.register(DataSet)
