from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from .models import Course_name
from Payments.models import Course_purchased
def course_purchased_required(view_func):
    @wraps(view_func)
    def wrapper(request, course_slug, topic_slug, *args, **kwargs):
        # Get the course based on the course_slug
        course = get_object_or_404(Course_name, slug=course_slug)

        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not logged in

        # Check if the user has purchased the course
        if not Course_purchased.objects.filter(user_id=request.user.id, course_id=course.id).exists():
            return redirect('start_course')  # Redirect to purchase page if course not purchased

        # Call the original view function
        return view_func(request, course_slug, topic_slug, *args, **kwargs)

    return wrapper
