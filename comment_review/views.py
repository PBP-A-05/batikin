from django.shortcuts import render, redirect
from comment_review.forms import ProductEntryForm
from comment_review.models import Product
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

@login_required
def create_review(request):
    form = ProductEntryForm(request.POST or None)

    if request.method == "POST":
        # Get the value of the custom input field
        review = request.POST.get("review", "")

        # Handle cancel button
        if 'cancel' in request.POST:
            return redirect('shopping:product_detail')

        # Handle submit button
        elif 'submit' in request.POST and form.is_valid():
            # Process form and save entry
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.review = review
            product_entry.save()

            return redirect('shopping:product_detail')

    context = {
        'form': form,
        'name': request.user.username,
    }
    return render(request, "create_product_entry.html", context)