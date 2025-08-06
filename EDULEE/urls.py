from django.urls import path
from .views import*

urlpatterns = [
    path('',home, name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('courses-details/<int:id>',courses_details,name='courses-details'),
    path('my-courses', render_course, name = 'my-courses'),
    path('blog/',blog,name='blog'),
    path('faq/',faq,name='faq'),
    path('404-error/',page_error,name='404-error'),
    path('blog-left-sidebar/',blog_left_sidebar,name='blog-left-sidebar'),
    path('blog-right-sidebar/',blog_right_sidebar,name='blog-right-sidebar'),
    path('student_corner/',student_corner,name='student_corner'),
    # path('start_course/',start_course,name="start_course"),
    path('render_course/<slug:slug>',render_course,name="render_course"),
    path('courses/<slug:course_slug>/<slug:topic_slug>/', play_course, name="courses"),
   path('all-courses-detail/', all_courses_detail, name='all-courses-detail'),
   path("services/", service_view, name="services"),


    path('instructor_dashboard/',instructor_dashboard,name='instructor_dashboard'),
    path('instructor_performance/',instructor_performance,name='instructor_performance'),
    path('students',students ,name='students'),
]
