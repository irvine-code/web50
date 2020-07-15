from django.contrib import admin
from .models import tweet,Comment, Preference

# Register your models here.
admin.site.register(tweet)
admin.site.register(Comment)
admin.site.register(Preference)