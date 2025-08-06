from django.contrib import admin
from .models import *



# class PaymentOrder_Admin(admin.ModelAdmin):
#     list_display = ('order_id', 'amount', 'status', 'created_at')
# admin.site.register(PaymentOrder,PaymentOrder_Admin)

class Course_purchasedAdmin(admin.ModelAdmin):
    ordering = ('-purchased_date',)
    empty_value_display = "--nill--"
    list_display=('course_name','course_price','username','purchased_date')
    search_fields=['username']
    list_filter=['course_name']
admin.site.register(Course_purchased,Course_purchasedAdmin)

