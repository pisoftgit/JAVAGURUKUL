from django.db import models

# Create your models here.

class PaymentOrder(models.Model):
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
    

class Course_purchased(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    username = models.CharField(max_length = 150)
    course_name = models.CharField(max_length=150)
    course_price = models.FloatField(null=True)
    order_id = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length=100,null=True)
    tax_amount = models.FloatField(null=True)
    tax_percentage = models.IntegerField(null=True)
    total_amount_paid = models.FloatField(null=True)
    currency  = models.CharField(max_length=50,null=True)
    purchased_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Course Purchased"
    class Meta:
        verbose_name_plural = "Course Purchased"

    