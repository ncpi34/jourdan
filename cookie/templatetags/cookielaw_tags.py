import warnings
from classytags.helpers import InclusionTag
from django import template
from django.template.loader import render_to_string

register = template.Library()


class CookielawBanner(InclusionTag):
    """
    Displays cookie law banner only if user has not dismissed it yet.
    """

    template = 'cookie/banner.html'

    def render_tag(self, context, **kwargs):
        template_filename = self.get_template(context, **kwargs)
        if 'request' not in context:
            warnings.warn('No request object in context. '
                          'Are you sure you have django.core.context_processors.request enabled?')
            return ''

        elif context['request'].COOKIES.get('cookielaw_accepted', False):
            return ''

        elif 'cookielaw_declined' in context['request'].COOKIES.values():
            return ''

        data = self.get_context(context, **kwargs)

        return render_to_string(template_filename, data, getattr(context, 'request', None))


register.tag(CookielawBanner)
