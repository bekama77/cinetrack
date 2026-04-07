from django import forms
from .models import WatchEntry, Collection

class WatchEntryForm(forms.ModelForm):
    class Meta:
        model = WatchEntry
        fields = ("movie", "status", "watched_at", "personal_note", "is_favorite")
        widgets = {
            "watched_at": forms.DateInput(attrs={"type": "date"}),
            "personal_note": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional note"}),
        }

class CollectionBaseForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ("title", "description", "is_public", "movies")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Collection title"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "What is this collection about?"}),
        }

class CollectionCreateForm(CollectionBaseForm):
    pass

class CollectionEditForm(CollectionBaseForm):
    pass
