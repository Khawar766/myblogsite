from typing import Union
from django.contrib.sitemaps import Sitemap
from .models import Blogpost

class BlogpostSitemap(Sitemap):
    def items(self):
        return Blogpost.objects.all()