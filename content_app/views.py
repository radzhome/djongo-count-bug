from django.views.generic.detail import DetailView

from .models import Content


class ContentAmpView(DetailView):
    """
    Content amp
    Template view endpoint, not included in drf UI or swagger atm
    """
    model = Content
    template_name = 'index.html'  # Defaults to content_detail.html
