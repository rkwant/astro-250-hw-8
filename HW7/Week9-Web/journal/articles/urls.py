from django.conf.urls.defaults import *

urlpatterns = patterns("articles.views",
    url(r"^(?P<slug>[-\w]+)/$", "detail", name="article_detail"),
)