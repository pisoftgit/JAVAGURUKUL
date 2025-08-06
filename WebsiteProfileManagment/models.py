from django.db import models



class Website_Manage(models.Model):
    phone_number = models.CharField(max_length=13, help_text = "phone number ex. +919001089265")
    email = models.EmailField(max_length=254,help_text = "Email ex. myemail@gmail.com")
    address_line_1 = models.CharField(max_length=150, help_text="ex. plot no 1, phase 2b Sas nagar")
    address_line_2 = models.CharField(max_length=150, help_text="ex. Mohali, Punjab 160071")
    powered_by = models.CharField(max_length=150, help_text="Powered by Company name. ex. Pisoft Informatics Pvt. Ltd.")
    powered_by_link = models.CharField(max_length=150, help_text="Link of Powered by Company ex. https://www.pisoftinformatics.com")
    def __str__(self):
        return "Website Profile Data"
    class Meta:
        verbose_name_plural = "Website Profile Info"

class Social_Links(models.Model):
    facebook_link = models.CharField(max_length=150, help_text="https://www.facebook.com/pisoftinformatics", default='#')
    linkedin_link = models.CharField(max_length=150, help_text="https://www.Linkedin.com/pisoftinformatics", default='#')
    twitter_link = models.CharField(max_length=150, help_text="https://www.twitter.com/pisoftinformatics", default='#')
    instagram_link = models.CharField(max_length=150, help_text="https://www.instagram.com/pisoftinformatics", default='#')
    skype_link = models.CharField(max_length=150, help_text="https://www.skype.com/pisoftinformatics", default='#')
    # TODO: Add youtube Link 
    def __str__(self):
        return "Social Links"
    class Meta:
        verbose_name_plural = "Social Links "