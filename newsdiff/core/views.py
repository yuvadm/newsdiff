import reversion

from django.views.generic import DetailView
from reversion.helpers import generate_patch_html
from reversion.models import Version
from .models import *


class HaaretzArticleView(DetailView):

    context_object_name = 'article'
    model = HaaretzArticle
    slug_field = 'haaretz_id'
    slug_url_kwarg = 'id'

    template_name = 'haaretz-article.html'

    def get_context_data(self, **kwargs):
        context = super(HaaretzArticleView, self).get_context_data(**kwargs)
        versions = reversion.get_for_object(self.object)
        version_diffs = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        context['diffs'] = [{
            'diff': generate_patch_html(v1, v2, 'text', cleanup='semantic')
        } for (v1, v2) in version_diffs]
        # context['diffs'] = [(v1, v2) for v1, v2 in zip(versions, versions[1:])]
        return context
