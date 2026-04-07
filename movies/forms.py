from django import forms
from django.utils import timezone
from .models import Movie

class MovieBaseForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            "title", "description", "release_year", "duration_minutes", "poster",
            "trailer_url", "genres", "is_featured", "is_public",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Movie title"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Movie summary"}),
            "release_year": forms.NumberInput(attrs={"placeholder": "Release year"}),
            "duration_minutes": forms.NumberInput(attrs={"placeholder": "Runtime in minutes"}),
            "trailer_url": forms.URLInput(attrs={"placeholder": "Optional trailer URL"}),
        }

    def clean_release_year(self):
        year = self.cleaned_data["release_year"]
        if year < 1888 or year > timezone.now().year:
            raise forms.ValidationError("Release year is outside the allowed range.")
        return year

class MovieCreateForm(MovieBaseForm):
    pass

class MovieEditForm(MovieBaseForm):
    pass

class MovieDeleteForm(MovieBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.required = False
