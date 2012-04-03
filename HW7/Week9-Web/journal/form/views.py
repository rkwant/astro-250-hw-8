from django import http
from django import forms as forms
 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from form.models import Document
from form.forms import DocumentForm

def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			f = request.FILES['docfile']
			
			
			#newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect('')
	else:
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
		'form/list.html',
		{'documents': documents, 'form': form},
		context_instance=RequestContext(request)
	)