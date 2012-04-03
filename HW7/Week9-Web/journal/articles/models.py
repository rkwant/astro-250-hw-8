from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Article(models.Model):
    title = models.CharField(_("title"), max_length=255, unique=True)
    slug = models.SlugField(_("slug"), unique=True)
    author = models.ForeignKey(User)
    published = models.DateTimeField(_("created"), default=datetime.now)
    
    abstract = models.TextField(_("abstract"))
    body = models.TextField(_("article body"))
    
    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
