from django.contrib import admin
from .models import *

# Register your models here.



class CoursesNameAdmin(admin.ModelAdmin):
    list_display=('course_name','course_name')
admin.site.register(Course_name, CoursesNameAdmin)


# Course Topics
class CourseTopics_Admin(admin.ModelAdmin):
    list_display=('course_name','title','tag')
    search_fields=['title']
    list_filter=['course_name']
admin.site.register(Course_topics,CourseTopics_Admin)


class InstructorAdmin(admin.ModelAdmin):
    list_display=('name','designation','rating')
    search_fields=('name','designation')
    list_filter=['name','rating']
admin.site.register(Instructors,InstructorAdmin)



class ContactAdmin(admin.ModelAdmin):
    list_display=('name','subject','timestamp')
admin.site.register(Contact,ContactAdmin)




class FAQItemInline(admin.StackedInline):
    model = FAQitems
    extra = 1

class FAQCategoryAdmin(admin.ModelAdmin):
    inlines = [FAQItemInline]
admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(FAQitems)
