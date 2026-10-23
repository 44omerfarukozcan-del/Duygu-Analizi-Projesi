from django.contrib import admin
from .models import Feedback, Institution, UserProfile

admin.site.register(Institution)
admin.site.register(UserProfile)
admin.site.register(Feedback)