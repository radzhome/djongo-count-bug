# Generated by Django 2.1.5 on 2019-02-01 01:50

from django.db import migrations, models
import djongo.models.json
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('_id', models.TextField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('titles', djongo.models.json.JSONField(default='{"main": "", "seo": ""}')),
                ('credits', djongo.models.json.JSONField(default='{"authors": []}')),
                ('taxonomies', djongo.models.json.JSONField(default='{"tags": [], "categories": []}')),
                ('content_elements', djongo.models.json.JSONField(default=[])),
                ('metadata', djongo.models.json.JSONField(default={}, null=True)),
                ('featured_media', djongo.models.json.JSONField(blank=True, default='{"image": ""}', null=True)),
                ('client_id', djongo.models.json.JSONField(default={}, null=True)),
                ('origin_id', models.IntegerField(null=True)),
                ('origin_url', models.TextField(blank=True, null=True)),
                ('origin_url_path', models.TextField(blank=True, null=True)),
                ('origin_cms', models.TextField(blank=True, null=True)),
                ('origin_slug', models.TextField(blank=True, null=True)),
                ('type', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=64)),
                ('version', models.TextField()),
                ('order', models.IntegerField(default=0, null=True)),
                ('excerpt', models.TextField(blank=True, null=True)),
                ('global_slug', models.TextField(blank=True, null=True)),
                ('nlp', djongo.models.json.JSONField(default='{"keyTopics": [], "categories": [], "entities": []}')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('published_on', models.DateTimeField(editable=False)),
                ('imported_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'content',
                'ordering': ['-_id'],
            },
        ),
    ]
