from json import dumps as json_dumps
# import html
# import datetime
import uuid

from djongo import models
from djongo.models import json
from django.urls import reverse
# from django.utils.timesince import timesince
# from django.utils import timezone
# from django.template.defaultfilters import truncatechars


class Content(models.Model):  # pragma: no cover

    _id = models.TextField(primary_key=True, default=uuid.uuid1, editable=False)
    titles = json.JSONField(default='{"main": "", "seo": ""}', null=False)
    credits = json.JSONField(default='{"authors": []}', null=False)
    taxonomies = json.JSONField(default='{"tags": [], "categories": []}')
    content_elements = json.JSONField(default=[], null=False)
    metadata = json.JSONField(default={}, null=True)
    featured_media = json.JSONField(default=json_dumps({'image': ''}), null=True, blank=True)
    client_id = json.JSONField(default={}, null=True)
    #license_id = models.ForeignKey('license_app.License', on_delete=models.CASCADE, blank=False, null=False,
    #                               db_column='license_id')
    origin_id = models.IntegerField(null=True)
    origin_url = models.TextField(null=True, blank=True)
    origin_url_path = models.TextField(null=True, blank=True)
    origin_cms = models.TextField(null=True, blank=True)
    origin_slug = models.TextField(null=True, blank=True)
    type = models.CharField( max_length=64, blank=False, null=False)
    status = models.CharField(max_length=64, blank=False, null=False)
    version = models.TextField(null=False, blank=False)
    order = models.IntegerField(null=True, default=0)
    excerpt = models.TextField(null=True, blank=True)
    global_slug = models.TextField(null=True, blank=True)
    nlp = json.JSONField(default='{"keyTopics": [], "categories": [], "entities": []}', null=False)

    # Dates
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
    published_on = models.DateTimeField(auto_now_add=False, editable=False)
    imported_on = models.DateTimeField(auto_now_add=False, editable=True, blank=False, null=False)

    class Meta:
        db_table = 'content'
        ordering = ['-_id']  # Needed for DRF pagination

    def __unicode__(self):
        return '{} {}: {}'.format(self.titles, self.type, self.status)

    @property
    def authors(self):
        return ' , '.join([author['name'] for author in self.credits['authors'] or []])

    @property
    def author_list(self):
        return [author['name'] for author in self.credits['authors']] or []

    @property
    def author(self):
        """
        Get main author
        """
        result = self.credits['authors'][0].get('name') if self.credits['authors'] else ''
        if result.startswith("By ") or result.startswith("by "):
            result = result[3:]
        return result

    @property
    def word_count(self):
        """
        :return: int, read time
        """
        word_count_num = 0
        words_per_minute = 225  # Average reading speed
        for item in self.content_elements:
            if item['type'] in STORY_ELEMENTS:
                word_count_num += len(item['content'].split(" "))
        read_time = round(word_count_num / words_per_minute)
        return read_time

    @property
    def secure_origin_url(self):
        """Get secure version of origin url"""
        return (self.origin_url).replace('http://', 'https://').replace('www.', '')

    @property
    def title(self):
        """Get main title"""
        return self.titles['main'] if 'main' in self.titles else ''


    @property
    def publisher(self):
        return self.metadata['pn_org'] if 'pn_org' in self.metadata else 'Postmedia'

    @property
    def image_url(self):
        return self.featured_media['image']['url'] if \
            self.featured_media and self.featured_media.get('image') else '#'

    @property
    def image_caption(self):
        return self.featured_media['image']['caption'] if \
            self.featured_media and self.featured_media.get('caption') else ''

    @property
    def category(self):
        """Get main category"""
        # TODO: There seems to be two schemas for categories
        # categories = self.taxonomies.get('categories') or {}
        # main_category = categories[0].get('main') if categories else ''
        # return main_category
        categories = self.taxonomies.get('categories') or []
        for c in categories:
            if c.get('main'):
                return c
                # return c.get('name')
        return {}

    @property
    def analytics_category(self):
        """
        Return the path as a list
        :return: dict, returns category names in lower case
        """
        if self.taxonomies is not None:
            categories = self.taxonomies.get('categories') or []
            for c in categories:
                if c.get('main') and c is not None:
                    parent_category = c.get('path', '').split('/') or []
                    hierarchy = list(filter(None, parent_category))
                    return [element.lower().replace('&amp;', '-') for element in hierarchy]
        else:
            return {}

    @property
    def ads_category(self):
        """
        :return: dict, returns main category and sub-categories except the last one.
        Retrieves and places the slug of the last sub-category
        """
        all_categories = []
        taxonomies = self.taxonomies or {}
        categories = taxonomies.get('main_taxonomies') or []
        for category in categories:
            if category.get('main'):
                split_categories = list(filter(None, category.get('path', '').split('/') or []))
                del split_categories[-1]
                split_categories.append(category.get('slug'))
                [element.replace('&amp;', '') for element in split_categories]
                if len(split_categories) == 1:
                    return split_categories[0], None
                else:
                    return split_categories[0], [element for element in split_categories[1:]]

        return all_categories

    @property
    def categories(self):
        taxonomies = self.taxonomies or {}
        return taxonomies.get('categories') or []
        # return '/'.join([c['slug'] for c in self.taxonomies.get('categories')]) if self.taxonomies.categories else ''

    @property
    def category_names(self):
        return list(filter(None, [tag['name'] for tag in self.categories]))

    @property
    def main_taxonomies(self):
        taxonomies = self.taxonomies or {}
        return taxonomies.get('main_taxonomies') or []

    @property
    def main_taxonomy_names(self):
        # Slug seems to be more descriptive than name
        return list(filter(None, [tag['slug'] for tag in self.main_taxonomies]))

    @property
    def tags(self):
        taxonomies = self.taxonomies or {}
        return taxonomies.get('tags') or []

    @property
    def tag_string(self):
        # Could be another function to return tag string. Not used.
        return '/'.join([c['slug'] for c in self.taxonomies.get('tags')]) if self.taxonomies.tags else ''

    @property
    def tag_names(self):
        return list(filter(None, [tag['name'] for tag in self.tags]))

    @property
    def headline(self):
        """headline, required for regwall"""
        return self.title

    @property
    def id(self):
        """Create id form _id, required for regwall"""
        return self._id

    def get_absolute_url(self):
        """get absolute url, required for regwall"""
        return self.get_amp_long_url()

    def get_amp_long_url(self):
        """get long url, for wp url compatibility"""
        return reverse('content-amp-long-url', args=[str(self.origin_url_path or 'article-slug'), str(self._id)])

    def get_html_long_url(self):
        """get long url, for wp url compatibility"""
        return reverse('content-html-long-url', args=[str(self.origin_url_path or 'article-slug'), str(self._id)])

    @property
    def get_generic_long_url(self):
        return self.get_amp_long_url().rstrip('/amp')

    @property
    def main_date(self):
        """Best available date to serve as date published"""
        return self.published_on or self.modified_on or self.created_on or self.imported_on


    @property
    def nlp_entities(self):
        """Extracts nlp entities from nlp"""
        nlp = self.nlp or {}
        nlp_entities = list(filter(None, nlp.get("entities") or []))
        # return [element.get('token') for element in nlp_entities]
        return ["{} {}".format(element.get('token'), element.get('type')) for element in nlp_entities]

    @property
    def nlp_keywords(self):
        """Extracts nlp keywords from nlp"""
        nlp = self.nlp or {}
        nlp_keywords = list(filter(None, nlp.get("keyTopics") or []))
        return [element.get('text') for element in nlp_keywords]

    @property
    def nlp_categories(self):
        """Extracts nlp categories from nlp"""
        nlp = self.nlp or {}
        nlp_categories = list(filter(None, nlp.get("categories") or []))
        return [element.get('name') for element in nlp_categories]

    @property
    def nlp_keywords_score(self):
        """Extract nlp keywords with score (seperated by comma) from nlp"""
        nlp = self.nlp or {}
        nlp_keywords = list(filter(None, nlp.get("keyTopics") or []))
        nlp_keywords_score = []
        for element in nlp_keywords:
            nlp_keywords_score.append(element.get('text')+", "+str(element.get('score'))) \
                if 'score' in element.keys() else nlp_keywords_score.append(element.get('text'))
        return nlp_keywords_score

    @property
    def nlp_entities_score(self):
        """Extract nlp entities with score (seperated by comma) from nlp"""
        nlp = self.nlp or {}
        nlp_entities = list(filter(None, nlp.get("entities") or []))
        nlp_entities_score = []
        for element in nlp_entities:
            nlp_entities_score.append(element.get('token')+", "+str(element.get('score'))) \
                if 'score' in element.keys() else nlp_entities_score.append(element.get('token'))
        return nlp_entities_score

    @property
    def nlp_categories_score(self):
        """Extract nlp categories with score (seperated by comma) from nlp"""
        nlp = self.nlp or {}
        nlp_categories = list(filter(None, nlp.get("categories") or []))
        nlp_categories_score = []
        for element in nlp_categories:
            nlp_categories_score.append(element.get('name')+", "+str(element.get('score'))) \
                if 'score' in element.keys() else nlp_categories_score.append(element.get('name'))
        return nlp_categories_score
