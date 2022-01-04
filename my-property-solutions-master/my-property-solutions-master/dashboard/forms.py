from django import forms

from my_property_solutions.forms import FormFormatter
from .models import NoteForMyself
class NoteForMyselfForm(FormFormatter):
    class Meta:
        fields = ["note"]
        model = NoteForMyself
        widgets = {"note": forms.Textarea(attrs={"cols": 100, "rows": 5})}
