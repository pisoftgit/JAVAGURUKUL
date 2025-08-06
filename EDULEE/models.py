from django.db import models
from tinymce.models import HTMLField

import os
from django.utils.text import slugify


class Instructors(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    image = models.ImageField(upload_to='author_images')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Team Members"



class Course_name(models.Model):  
    course_name = models.CharField(max_length=150)
    author = models.ManyToManyField(Instructors)
    tag = models.CharField(max_length=50)
    duration = models.CharField(max_length=20)
    lectures = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.IntegerField()
    image = models.ImageField(upload_to='courses_images')
    author_image = models.ImageField(upload_to='author_images')
    course_description = HTMLField(null=True, blank=True)
    course_pricing = models.BooleanField(help_text='Check me if Course is Paid')
    slug = models.SlugField(unique=True, blank=True, null=True,max_length=150)

    class Meta:
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class Course_topics(models.Model):
    course_name = models.ForeignKey(Course_name, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, help_text="Example - java, python or c")
    image = models.ImageField(upload_to='courses_images', help_text="Video Thumbnail Image")
    video_link = models.CharField(max_length=150, blank=True, null=True, help_text="Enter Youtube Link only and copy link from embed option of youtube.")
    video_file = models.FileField(upload_to="course_videos/", blank=True, null=True, help_text="Upload the video file (if available)")
    video_description = HTMLField(blank=True, null=True)
    resources = HTMLField(blank=True, null=True)
    notes = HTMLField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True,help_text="write your custom url ex. introduction-to-java or keep it blank")  # Make slug nullable


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Course Topics"
        

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug based on title
            self.slug = slugify(self.title)
        super(Course_topics, self).save(*args, **kwargs)




# class Course_purchased(models.Model):
#     course_id = models.IntegerField()
#     course_name = models.CharField(max_length=150)
#     course_price = models.CharField(max_length=50)
#     course_old_price = models.CharField(max_length = 50)
#     username = models.CharField(max_length = 150)
#     user_id = models.IntegerField(unique = False)
#     purchased_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "Course Purchased"
#     class Meta:
#         verbose_name_plural = "Course Purchased"



class Course(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='media/img')  # Assuming images are uploaded to 'author_images' directory
    completion_percentage = models.IntegerField(default=0)
    rating_percentage = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media/img')  # Assuming images are uploaded to 'course_images' directory
    def __str__(self):
        return self.title





class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=200)
    message=models.TextField(max_length=500)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"

    class Meta:
        verbose_name_plural= "Contact Form Data"


class FAQCategory(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="FAQ Category"

class FAQitems(models.Model):
    category=models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question=models.CharField(max_length=500)
    answer=models.TextField()

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural="FAQ Items"


