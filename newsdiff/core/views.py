import reversion

from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, ListView
from reversion.helpers import generate_patch_html
from reversion.models import Version
from .models import *


class ArticleView(DetailView):
    context_object_name = 'article'
    slug_url_kwarg = 'id'
    template_name = 'article.html'

    def _get_diffs(self):
        versions = reversion.get_for_object(self.object)
        version_diffs = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        return [{
            'diff': generate_patch_html(v2, v1, 'text', cleanup='semantic'),
            'date': v1.revision.date_created
        } for (v1, v2) in version_diffs]

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['diffs'] = self._get_diffs()
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

    def _get_latest_revisions(self):
        model_content_type = ContentType.objects.get_for_model(self.model)
        versions = Version.objects.filter(content_type=model_content_type).order_by('-revision__date_created')
        return versions

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['latest_revisions'] = self._get_latest_revisions()
        return context


class HaaretzListView(ArticleListView):
    model = HaaretzArticle
    queryset = HaaretzArticle.objects.order_by('-date')


class YnetListView(ArticleListView):
    model = YnetArticle
    queryset = YnetArticle.objects.order_by('-date')
