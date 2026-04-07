from django import forms
from .models import Review

class ReviewBaseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("movie", "title", "content", "rating")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Review title"}),
            "content": forms.Textarea(attrs={"rows": 5, "placeholder": "What did you think?"}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

class ReviewCreateForm(ReviewBaseForm):
    pass

class ReviewEditForm(ReviewBaseForm):
    pass
