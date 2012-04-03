from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from articles.models import Article

def articles(request, template_name="articles/list.html"):
    articles = Article.objects.all()
    
    return render_to_response(template_name, {
        'articles': articles,
    }, context_instance=RequestContext(request))

def detail(request, slug=None, template_name="articles/detail.html"):
    article = get_object_or_404(Article, slug=slug)
    
    return render_to_response(template_name, {
        'article': article,
    }, context_instance=RequestContext(request))