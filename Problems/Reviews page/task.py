from django.shortcuts import render
from django.views import View


class ReviewView(View):
    reviews = []  # List of reviews as plain strings

    def get(self, request, *args, **kwargs):
        reviews = "review"
        return render(request, "book/reviews.html", context={"reviews": reviews})