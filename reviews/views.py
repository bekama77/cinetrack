from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ReviewCreateForm, ReviewEditForm
from .models import Review

class ReviewOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

class ReviewListView(ListView):
    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(is_hidden=False).select_related("movie", "user")

class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("reviews:review-list")
    success_message = "Review created."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, ReviewOwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("reviews:review-list")
    success_message = "Review updated."

class ReviewDeleteView(LoginRequiredMixin, ReviewOwnerRequiredMixin, DeleteView):
    model = Review
    template_name = "reviews/review_confirm_delete.html"
    success_url = reverse_lazy("reviews:review-list")
