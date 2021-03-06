import reversion

from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from django.views.generic import DetailView, ListView
from reversion.helpers import generate_patch_html
from reversion.models import Version
from .models import *
from .tasks import process_haaretz_article


class ArticleView(DetailView):
    context_object_name = 'article'
    slug_url_kwarg = 'id'
    template_name = 'article.html'

    def _get_diffs(self):
        versions = reversion.get_for_object(self.object)
        version_diffs = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        return [{
            'title_diff': generate_patch_html(v2, v1, 'title', cleanup='semantic'),
            'subtitle_diff': generate_patch_html(v2, v1, 'subtitle', cleanup='semantic'),
            'text_diff': generate_patch_html(v2, v1, 'text', cleanup='semantic'),
            'date': v1.revision.date_created
        } for (v1, v2) in version_diffs]

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['diffs'] = self._get_diffs()
        return context


class HaaretzArticleView(ArticleView):
    model = HaaretzArticle
    slug_field = 'haaretz_id'

    def get_object(self, queryset=None):
        try:
            return super(HaaretzArticleView, self).get_object(queryset=queryset)
        except Http404 as e:
            if not self.request.user.is_authenticated():
                raise e
            else:
                id = self.kwargs.get(self.slug_url_kwarg, None)
                process_haaretz_article.delay('http://www.haaretz.co.il/{}'.format(id))
                raise Http404('Attempting to fetch haaretz article')

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated() and request.POST.get('star'):
            article = self.get_object()
            article.starred = True
            article.save()
            return HttpResponse('starred')
        return HttpResponse('ok')


class YnetArticleView(ArticleView):
    model = YnetArticle
    slug_field = 'ynet_id'


class ArticleListView(ListView):
    context_object_name = 'articles'
    template_name = 'articles.html'
    paginate_by = 100

    def _get_latest_revisions(self):
        model_content_type = ContentType.objects.get_for_model(self.model)
        versions = Version.objects.filter(content_type=model_content_type).order_by('-revision__date_created')[:self.paginate_by]
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
