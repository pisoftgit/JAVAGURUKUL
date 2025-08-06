# # Checkout Page for Payments (Subtotal, GST and all other Taxes)


# from django.shortcuts import render, redirect,get_object_or_404

# def start_course(request):
#     if request.user.is_authenticated:
#             print(request.method)
#             if request.method == 'GET':
                
#                 cd_id  = request.GET.get('cd-id')
#                 cd_name  = request.GET.get('cd-name')
#                 cd_oldprice = request.GET.get('cd-oldprice')
#                 cd_price = float(request.GET.get('cd-price'))
#                 tax  = 18
                
#                 total_tax = ((cd_price)*tax)/100
#                 total_price = total_tax + float(cd_price)
#                 if Course_purchased.objects.filter(user_id=request.user.id, course_id=cd_id).exists():
#                     messages.info(request, 'Course Already Purchased....!!')
#                     return redirect('student_corner')
               
#                 context = {
#                     'course_id' : cd_id,
#                     'cd_name' : cd_name,
#                     'cd_oldprice' : cd_oldprice,
#                     'cd_price' : cd_price,
#                     'tax_persnt' : tax,
#                     'cd_tax' : total_tax,
#                     'total_price' : total_price,
#                 }
#                 request.session['session_data'] = context
#                 currency = 'INR'
#                 amount = total_price*100
#                 order_name  = cd_name
#                 razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                                 currency=currency,
#                                                                 payment_capture='1'))
                
#                 # order id of newly created order.
#                 # print(razorpay_order)
#                 razorpay_order_id = razorpay_order['id']
#                 callback_url = '/payments/payment-success'
            
                
#                 context['razorpay_order_id'] = razorpay_order_id
#                 context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
#                 context['razorpay_amount'] = amount 
#                 context['currency'] = currency
#                 context['order_name'] = order_name
#                 context['callback_url'] = callback_url
            
#                 PaymentOrder.objects.create(order_id = razorpay_order_id, amount = amount/100, currency = currency)
            
                
#                 return render(request,'start_course.html',context)

#     else:
#         return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings

def start_course(request):
    if request.user.is_authenticated:
        print(request.method)
        if request.method == 'GET':
            cd_id = request.GET.get('cd-id')
            cd_name = request.GET.get('cd-name')
            cd_oldprice = request.GET.get('cd-oldprice')
            cd_price_str = request.GET.get('cd-price')  # Use string version first
            
            if not cd_price_str:
                messages.error(request, "Course price is missing.")
                return redirect('student_corner')

            try:
                cd_price = float(cd_price_str)
            except ValueError:
                messages.error(request, "Invalid course price.")
                return redirect('student_corner')

            tax = 18
            total_tax = (cd_price * tax) / 100
            total_price = total_tax + cd_price

            if Course_purchased.objects.filter(user_id=request.user.id, course_id=cd_id).exists():
                messages.info(request, 'Course Already Purchased....!!')
                return redirect('student_corner')

            context = {
                'course_id': cd_id,
                'cd_name': cd_name,
                'cd_oldprice': cd_oldprice,
                'cd_price': cd_price,
                'tax_persnt': tax,
                'cd_tax': total_tax,
                'total_price': total_price,
            }

            request.session['session_data'] = context
            currency = 'INR'
            amount = int(total_price * 100)  # convert to paise

            order_name = cd_name
            razorpay_order = razorpay_client.order.create(dict(
                amount=amount,
                currency=currency,
                payment_capture='1'
            ))

            razorpay_order_id = razorpay_order['id']
            callback_url = '/payments/payment-success'

            context.update({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                'razorpay_amount': amount,
                'currency': currency,
                'order_name': order_name,
                'callback_url': callback_url
            })

            PaymentOrder.objects.create(
                order_id=razorpay_order_id,
                amount=amount / 100,
                currency=currency
            )

            return render(request, 'start_course.html', context)
    else:
        return redirect('login')
