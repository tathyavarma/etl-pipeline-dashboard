from django.contrib import admin

# Register your models here.
from .models import ETLJob

admin.site.register(ETLJob)