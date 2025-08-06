from .models import *


def website_data(request):
    try:
        company_info = Website_Manage.objects.first()  # Fetch the company information from your database
        company_social_profile = Social_Links.objects.first()  # Fetch the company information from your database
    except Website_Manage.DoesNotExist and Social_Links.DoesNotExist:
        company_info,company_social_profile = None, None
    return {
        'company_info': company_info,
        'company_social_profile'  : company_social_profile
    }