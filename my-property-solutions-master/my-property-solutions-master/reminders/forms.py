from django import forms
from .models import Reminders
class ReminderForm(forms.ModelForm):
    date = forms.DateField()
    time = forms.TimeField()
    class Meta:
        fields = ["date", "time", "notes"]
        model = Reminders

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.fields["date"].widget.attrs["placeholder"] = "Date"
        self.fields["date"].widget.attrs["autocomplete"] = "off"
        self.fields["time"].widget.attrs["placeholder"] = "Time"
        self.fields["notes"].widget.attrs["placeholder"] = "Notes"
