from django import forms


class FormFormatter(forms.ModelForm):
    """This is intended to provide common form formatting functions."""

    def __init__(self, *args, **kwargs):
        super(FormFormatter, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control "
            field.widget.attrs["placeholder"] = field.label
