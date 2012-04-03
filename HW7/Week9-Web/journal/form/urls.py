from django.conf.urls.defaults import *

urlpatterns = patterns("form.views",
    url(r"^fileupload/$", "list", name="list"),
)