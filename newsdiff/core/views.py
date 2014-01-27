import reversion

from django.views.generic import DetailView, ListView
from reversion.helpers import generate_patch_html
from reversion.models import Version
from .models import *


class ArticleView(DetailView):
    context_object_name = 'article'
    slug_url_kwarg = 'id'
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        versions = reversion.get_for_object(self.object)
        version_diffs = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        context['diffs'] = [{
            'diff': generate_patch_html(v2, v1, 'text', cleanup='semantic')
        } for (v1, v2) in version_diffs]
        # context['diffs'] = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        return context


class HaaretzArticleView(ArticleView):
    model = HaaretzArticle
    slug_field = 'haaretz_id'


class YnetArticleView(ArticleView):
    model = YnetArticle
    slug_field = 'ynet_id'


class ArticleListView(ListView):
    context_object_name = 'articles'
    template_name = 'articles.html'
    paginate_by = 10


class HaaretzListView(ArticleListView):
    model = HaaretzArticle
    queryset = HaaretzArticle.objects.order_by('-date')


class YnetListView(ArticleListView):
    model = YnetArticle
    queryset = YnetArticle.objects.order_by('-date')
