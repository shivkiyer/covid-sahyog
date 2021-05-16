from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

# Create your models here.

User = get_user_model()

class State(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class RequestHelpManager(models.Manager):
    def get_enabled(self):
        return self.get_queryset().filter(
            is_disabled=False
        )

    def get_verified(self):
        return self.get_enabled().filter(
            verified=True
        )


class RequestHelp(models.Model):
    help_choices = [
        ('medicines', 'Medicines'),
        ('hospital', 'Hospital'),
        ('oxygen', 'Oxygen'),
        ('food', 'Food'),
        ('ambulance', 'Ambulance'),
        ('blood', 'Blood/Plasma'),
        ('financial', 'Financial'),
        ('other', 'Other')
    ]
    display_name    = models.CharField(max_length=200)
    twitter_handle  = models.CharField(max_length=200, blank=True, null=True)
    mobile_number   = models.BigIntegerField(blank=True, null=True)
    email           = models.EmailField(blank=True, null=True)
    description     = models.TextField()
    help_needed     = models.CharField(
        max_length=20,
        choices=help_choices,
        default='oxygen'
    )
    is_help_offered = models.BooleanField(default=False)
    state           = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    address         = models.TextField()
    city            = models.CharField(max_length=200)
    assistance_url  = models.URLField(blank=True, null=True)
    created_on      = models.DateTimeField(auto_now_add=True)
    start_date      = models.DateTimeField(blank=True, null=True)
    end_date        = models.DateTimeField(blank=True, null=True)
    verified_on     = models.DateTimeField(auto_now=True, blank=True, null=True)
    verified        = models.BooleanField(default=False)
    verified_by     = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_disabled     = models.BooleanField(default=False)

    # Model manager
    objects = RequestHelpManager()

    # Ordering
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        help_type = ' offers ' if self.is_help_offered else ' needs '
        return self.display_name + ' in ' + self.city + ', ' + self.state.name + help_type + self.help_needed

    def validation_email(self, request):
        help_type = ' offers ' if self.is_help_offered else ' needs '
        subject = self.display_name + ' in ' + self.city + ', ' + self.state.name + help_type + self.help_needed
        message = 'The following request/offer has been submitted\n'
        message += request.build_absolute_uri(reverse('edit_help', args=[self.id])) + '\n'
        message += 'Name: ' + self.display_name + '\n'
        message += 'Mobile: ' + str(self.mobile_number) + '\n'
        message += 'Twitter: ' + self.twitter_handle + '\n'
        message += 'Email: ' + self.email + '\n'
        message += 'State: ' + self.state.name + ', City: ' + self.city + '\n'
        message += 'Help type: ' + self.help_needed + '\n'
        message += 'Address: ' + self.address + '\n'
        message += 'Description: ' + self.description + '\n'
        if self.start_date and self.end_date:
            message += 'Between ' + str(self.start_date) + ' and ' + str(self.end_date) + '\n'
        recipients = [settings.EMAIL_ADMIN_NOTIFICATION]
        return {
            'subject': subject,
            'message': message,
            'recipients': recipients
        }
