from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
# This is your test secret API key.
from django.contrib import messages

from django.http import HttpResponseBadRequest,JsonResponse
import hmac, hashlib
from .models import *
from EDULEE.models import Course_name
# Razorpay Payment 
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 


# Checkout Page for Payments (Subtotal, GST and all other Taxes)
def start_course(request):
    if request.user.is_authenticated:
          
            if request.method == 'POST':
                print(request.POST)
                cd_id  = request.POST.get('cd-id')
                cd_name  = request.POST.get('cd-name')
                cd_oldprice = request.POST.get('cd-oldprice')
                cd_price = float(request.POST.get('cd-price'))
                tax  = 18
                
                total_tax = ((cd_price)*tax)/100
                total_price = total_tax + float(cd_price)
                if Course_purchased.objects.filter(user_id=request.user.id, course_id=cd_id).exists():
                    messages.info(request, 'Course Already Purchased....!!')
                    return redirect('student_corner')
               
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
                
                # order id of newly created order.
                # print(razorpay_order)
                razorpay_order_id = razorpay_order['id']
                callback_url = '/payments/payment-success'
            
                
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
                context['razorpay_amount'] = amount 
                context['currency'] = currency
                context['order_name'] = order_name
                context['callback_url'] = callback_url
            
                PaymentOrder.objects.create(order_id = razorpay_order_id, amount = amount/100, currency = currency)
            
                
                return render(request,'start_course.html',context)
    else:
        return redirect('login')



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            # print(request.POST)  # Debugging: Print received POST data
            session_data = request.session.get('session_data')
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            razorpay_signature = request.POST.get('razorpay_signature', '')

            # Check if the context data exists in the session
            if session_data:
                # Access the individual values from the context dictionary
                course_id = session_data.get('course_id')
                cd_name = session_data.get('cd_name')
                cd_oldprice = session_data.get('cd_oldprice')
                cd_price = session_data.get('cd_price')
                cd_tax = session_data.get('cd_tax')
                total_price = session_data.get('total_price')
                tax_persnt = session_data.get('tax_persnt')
                currency = session_data.get('currency')
                try:
                
                    create_data = Course_purchased(
                        user_id=request.user.id,
                        course_id=course_id,
                        username=request.user.username,
                        course_name = cd_name,
                        course_price=cd_price,
                        order_id=razorpay_order_id,
                        payment_id=payment_id,
                        tax_amount=cd_tax,
                        tax_percentage=tax_persnt,
                        total_amount_paid = total_price,
                        currency = currency
                    )
                    create_data.save()


                    # Redirect to student corner after successful purchase
                    messages.success(request, 'Coursed Purchased Successfully....!!')
                    return redirect('student_corner')

                except Course_name.DoesNotExist:
                    return render(request, 'start_course.html', {'error': 'Selected course does not exist'})

                except Exception as error:
                    print(error)

              
            else:
                # Handle the case where the context data doesn't exist in the session
                # Maybe redirect the user to a page where they can provide this data again
                return HttpResponse(request,'Sory something went wrong')

        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    


def payment_cancel(request):
    return HttpResponse("Payment Canceled...!!!!")


