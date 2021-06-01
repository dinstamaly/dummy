from django.forms import ModelForm, NumberInput, Select
from .models import Column_m, DataSet


class ColumnForm(ModelForm):
    class Meta:
        model = Column_m
        fields = (
            'name', 'data_type', 'from_int', 'to_int', 'order',
        )
        widgets = {
            'data_type': Select(
                attrs={"id": "range", "onchange": "what_type()"}),
            'from_int': NumberInput(),
            'to_int': NumberInput(),
        }


class DataSetCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_row'].widget.attrs.update({'class': 'form-control'})
        self.fields['num_row'].label = 'Rows:'

    class Meta:
        model = DataSet
        fields = ('num_row',)
