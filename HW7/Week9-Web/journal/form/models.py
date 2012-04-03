from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
	
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	
class BibTexEntry(models.Model):
	title = models.CharFied()