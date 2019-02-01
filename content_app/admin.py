from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Content


class ContentAdmin(admin.ModelAdmin):
    """ContentAdmin class that contains the rendering logic for content in Content App."""

    list_display = ['get_title', 'modified_on', 'published_on', 'imported_on', '_id', 'show_amp_url', 'show_html_url']
    view_on_site = False

    def get_object(self, request, object_id, from_field=None):
        """
        Return an instance matching the field and value provided, the primary key is used if no field is provided.

        :param request: request
        :param object_id: Id of the content object
        :param from_field: from_field
        :return: dict; ``None`` if no match is found or the object_id fails validation.
        """
        obj = super(ContentAdmin, self).get_object(request, object_id, from_field)
        # Fix handling of Timestamp.
        # TODO: Would be nice to include this in default json serializer in django but can't seem
        # to find an option to overwrite this like we have in drf
        # https://docs.djangoproject.com/en/dev/topics/serialization/#djangojsonencoder
        if obj.nlp and 'created_at_ts' in obj.nlp:
            obj.nlp['created_at_ts'] = str(obj.nlp['created_at_ts']).replace(", 0)", '').replace("Timestamp(", '')
        return obj

    def get_form(self, request, obj=None, **kwargs):
        """To return form with field attributes."""
        has_perm = self.has_add_permission(request) or self.has_change_permission(request)
        form = super(ContentAdmin, self).get_form(request, obj, **kwargs)
        if has_perm:  # add or change
            form.base_fields['client_id'].label_from_instance = lambda obj: "{} {}".format(obj._id, obj.name)
            # form.base_fields['license_id'].label_from_instance = lambda obj: "{} {}".format(obj._id, obj.name)
            form.base_fields['titles'].widget = forms.Textarea()
            form.base_fields['titles'].required = True
            form.base_fields['credits'].widget = forms.Textarea()
            form.base_fields['credits'].required = True
            form.base_fields['taxonomies'].widget = forms.Textarea()
            form.base_fields['taxonomies'].required = False
            form.base_fields['content_elements'].widget = forms.Textarea()
            form.base_fields['content_elements'].required = True
            form.base_fields['metadata'].widget = forms.Textarea()
            form.base_fields['metadata'].required = False
            form.base_fields['featured_media'].widget = forms.Textarea()
            form.base_fields['featured_media'].required = False
            form.base_fields['nlp'].widget = forms.Textarea()
            form.base_fields['nlp'].required = False

        return form

    def get_title(self, obj):
        """To return title."""
        if obj.titles:
            titles = dict(obj.titles)
            list_titles = []
            if titles.get('main'):
                list_titles.append(titles['main'])
            if titles.get('seo'):
                list_titles.append(titles['seo'])
            if list_titles:
                return ' - '.join(list_titles)

        return 'N/A'

    get_title.short_description = 'Title'
    get_title.admin_order_field = 'titles'

    def show_amp_url(self, obj):
        """To return amp_url."""
        return format_html('<a href="{}" target="_blank">*</a>'.format(obj.get_amp_long_url()))

    show_amp_url.mark_safe = True
    show_amp_url.short_description = "AMP URL"

    def show_html_url(self, obj):
        """To Show html_url."""
        return format_html('<a href="{}" target="_blank">*</a>'.format(obj.get_html_long_url()))

    show_html_url.mark_safe = True
    show_html_url.short_description = "HTML URL"

    search_fields = ('_id', )


admin.site.register(Content, ContentAdmin)
