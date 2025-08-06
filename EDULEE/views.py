from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
import razorpay

from .models import *
from django.contrib.auth.decorators import login_required
from EDULEE.decorators import * 
from Payments.models import Course_purchased
import json

from django.db.models import Q
# Create your views here.

# Razorpay Payment 
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 



def home(request):
    # Fetch all unique course names directly from the database
    unique_course_names = Course_name.objects.values_list('course_name', flat=True).distinct()
    unique_courses_dict = Course_name.objects.all()
    context = {
        'unique_course_names': unique_course_names,
        'course': unique_courses_dict,
        
        #photos missing
    }

    return render(request, 'index.html', context)


def about(request):
    team_members=Instructors.objects.all()
    return render(request,'about.html',{'team_members':team_members})
# def all_courses_detail(request):
#     unique_course_names = Course_name.objects.values_list('course_name', flat=True).distinct()
#     unique_courses_dict = Course_name.objects.all()
#     context = {
#         'unique_course_names': unique_course_names,
#         'course': unique_courses_dict,
#     }

#     return render(request, 'all-courses-detail.html', context)
def all_courses_detail(request):
    unique_course_names = Course_name.objects.values_list('course_name', flat=True).distinct()
    unique_courses_dict = Course_name.objects.all()

    # Add half_rating (divided by 2) and star_width (percentage)
    for course in unique_courses_dict:
        if course.rating:
            course.half_rating = round(course.rating / 2, 1)
            course.star_width = (course.rating / 2) * 20  # scale to 100%
        else:
            course.half_rating = 0
            course.star_width = 0

    context = {
        'unique_course_names': unique_course_names,
        'course': unique_courses_dict,
    }

    return render(request, 'all-courses-detail.html', context)




def courses_details(request, id):
    course = Course_name.objects.get(id = id)
    is_coursepaid =  course.course_pricing
    # print(is_coursepaid)
    if course.rating:
        course.half_rating = round(course.rating / 2, 1)
        course.star_width = (course.rating / 2) * 20  # Convert to percent
    else:
        course.half_rating = 0
        course.star_width = 0

    course_topics = Course_topics.objects.filter(course_name_id = course.id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            tax = 18
            currency = 'INR'
            cd_id = request.POST.get('cd-id')
            cd_name =  request.POST.get('cd-name')
            cd_price = request.POST.get('cd-price')
            cd_oldprice = request.POST.get('cd-oldprice')
            total_tax = (float(cd_price)*tax)/100
            total_price = total_tax + float(cd_price)
            
            # Check if course is Free or Paid 
            if is_coursepaid == True:
                if Course_purchased.objects.filter(user_id=request.user.id, course_id=cd_id).exists():
                        messages.error(request, 'Course Already Purchased....!!', extra_tags="This Course is Already Purchased... You Don't Need To Purchase it Again...!!!")
                        return redirect('student_corner')
                
                
                total_price = total_tax + float(cd_price)
                context = {
                        'course_id' : cd_id,
                        'cd_name' : cd_name,
                        'cd_oldprice' : cd_oldprice,
                        'cd_price' : cd_price,
                        'tax_persnt' : tax,
                        'cd_tax' : total_tax,
                        'total_price' : total_price,
                    }
                request.session['session_data'] = context
                
                currency = 'INR'
                amount = total_price*100
                order_name  = cd_name
                
                razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                    currency=currency,
                                                                    payment_capture='1'))
                    
                
                razorpay_order_id = razorpay_order['id']
                callback_url = '/payments/payment-success'
                    
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
                context['razorpay_amount'] = amount 
                context['currency'] = currency
                context['order_name'] = order_name
                context['callback_url'] = callback_url
            
                return render(request,'start_course.html',context =  context)
            
            #  If Course is Free
            else:
                if Course_purchased.objects.filter(user_id=request.user.id, course_id=cd_id).exists():
                        messages.info(request, 'Course Already Purchased....!!', extra_tags="This Course is Already Purchased... You Don't Need To Purchase it Again...!!!")
                        return redirect('student_corner')
                create_data = Course_purchased(
                                user_id=request.user.id,
                                course_id=cd_id,
                                username=request.user.username,
                                course_name = cd_name
                            )
                create_data.save()
                messages.success(request, 'Coursed Purchased Successfully....!!', extra_tags="Now you can start Watching your purchased Course..")
                return redirect('student_corner')
            
        # If user is not authenticated
        else:
            return redirect('login')

    return render(request,'courses-details.html', {'Coursedata':course, 'data':course_topics})


def render_course(request, slug):
    course = get_object_or_404(Course_name, slug=slug)
    course_topics = Course_topics.objects.filter(course_name_id=course.id)
    return render(request, 'courses/render-courses.html', {'course': course, 'course_topics':course_topics})

@course_purchased_required
def play_course(request, course_slug, topic_slug):
    course = get_object_or_404(Course_name, slug=course_slug)
    course_topic = get_object_or_404(Course_topics, slug=topic_slug, course_name=course)
    
    # Filter Course_topics queryset based on the selected Course_name
    course_topics = Course_topics.objects.filter(course_name=course)
    
    return render(request, 'courses/play_course.html', {'course': course, 'course_topic': course_topic, 'course_topics': course_topics})

def blog(request):
    return render(request,'blog.html')

def service_view(request): 
    service = request.GET.get('service')

    services_data = {
        "online-java-courses": {
            "title": "Online Java Courses (Free & Paid)",
            "description": "Master Java from scratch through our structured and practical video tutorials on YouTube. From Core Java to advanced frameworks like Spring Boot, our content is beginner-friendly yet industry-relevant.",
            "image": "img/java1.jpg"
        },
        "mentorship": {
            "title": "Live Doubt Clearing/Mentorship",
            "description": "Get personalized support through live doubt-clearing sessions and one-on-one mentorship. Our guidance helps you overcome coding challenges and build a strong Java foundation.",
            "image": "img/mentorship.jpg"
        },
        "project-training": {
            "title": "Project-Based Training",
            "description": "Enhance coding and problem-solving skills with real-time Java projects. From mini to major, each follows industry standards. Build a powerful portfolio that showcases your talent beyond a traditional resume.",
            "image": "img/projectbased.jpg"
        },
        "certification": {
            "title": "Certification Programs",
            "description": "Earn industry-recognized certificates upon successful course or project completion.Our certifications validate your Java skills and add credibility to your resume.Stand out to employers with proof of practical, hands-on expertise.",
            "image": "img/certificates.jpg"
        },
        "internship": {
            "title": "Internship & Industrial Training",
            "description": "Join our 3 or 6-month internship program specially designed for MCA/BCA/B.Tech students. Gain real-world experience through a structured syllabus, daily tasks, and hands-on projects that connect academic learning with industry skills.",
            "image": "img/internship&t.jpg"
        },
        "job-prep": {
            "title": "Job Preparation Services",
            "description": "Crack Java interviews with our dedicated job-prep resources, mock tests, and resume support.Learn commonly asked questions, coding rounds, and system design essentials.We help you become job-ready with the skills companies actually look for.",
            "image": "img/course-2.jpg"
        }
    }

    selected_service = services_data.get(service)

    return render(request, 'services.html', {
        'selected_service': selected_service,
        'selected_slug': service,
        'services_data': services_data
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        try:
            send_data = Contact(name = name, subject = subject, email = email, message = message )
            send_data.save()
            messages.success(request, "Form Submited Successfully !! ")
            # current_site = get_current_site(request)
            # mail_subject = subject
            
            # message = f"Message from {name} ({email}): {message}"
            # email = EmailMessage(
            #     mail_subject,   
            #     message,        # HTML Content
            #     to=[email]   # Recipient
            # )
            # email.content_subtype = "html"  # Set the content type to HTML
            # email.send()


            # return redirect('contact')
        except :
            messages.error(request, "Something Went Wrong !! ")
            
            return redirect('contact')


    return render(request,'contact.html') 


def faq(request):
    unique_faq_categories = FAQCategory.objects.all()

    # Create a dictionary to store FAQ items for each category
    faq_dict = {}
    for faq_category in unique_faq_categories:
        faq_dict[faq_category] = FAQitems.objects.filter(category=faq_category)

    context = {
        'unique_faq_categories': unique_faq_categories,
        'faq_dict': faq_dict,
    }

    return render(request, 'faq.html', context)

def page_error(request):
    return render(request,'404-error.html')

def blog_left_sidebar(request):
    return render(request,'blog-left-sidebar.html')

def blog_right_sidebar(request):
    return render(request,'blog-right-sidebar.html')

def blog_details_left_sidebar(request):
    return render(request, 'blog-details-left-sidebar.html')


def student_corner(request):
    if request.user.is_authenticated:
        user = request.user
        purchased_courses = Course_purchased.objects.filter(user_id=user.id)
        courses_details = Course_name.objects.filter(pk__in=purchased_courses.values_list('course_id', flat=True))

        context = {
            'purchased_courses': purchased_courses,
            'courses': courses_details,
        }

        return render(request, 'student_corner.html', context)
    else:
        return redirect('login')
 

def instructor_dashboard(request):
    return render(request,'admin/instructor_dashboard.html')

def instructor_performance(request):
    return render(request,'admin/instructor_performance.html')

def students(request):
    return render(request,'admin/students.html')
    


