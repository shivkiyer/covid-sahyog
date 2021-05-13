from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class State(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.display_name + ' in ' + self.city + ', ' + self.state.name + ' needs ' + self.help_needed
