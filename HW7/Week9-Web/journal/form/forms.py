from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a file',
	)
	
	collection = forms.CharField(
		label='Collection',
		help_text='Please enter a collection name'
	)