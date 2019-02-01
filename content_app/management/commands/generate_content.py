"""
Generate lots of content to mongodb
"""
import datetime
import json
import math
import time
import copy

from django.core.management.base import BaseCommand

from content_app.models import Content

CONTENT_TEMPLATE = {
    "type": "story",
    "modified_on": datetime.datetime.now(),
    "published_on": datetime.datetime.now(),
    "status": "draft",
    "titles": {
        "main": "Test title blah blah"
    },
    "credits": {
        "authors": [
        ]
    },
    "content_elements": [
        {
            "content": "Some test content",
            "paragraph": "wrap",
            "type": "text",
            "channels": [
                "desktop",
                "tablet",
                "phone"
            ],
            "_id": "1"
        },

    ],
    "taxonomies": {
        "tags": [
        ],
        "categories": [],
        "main_taxonomies": []
    },
    "metadata": {
    },
    "version": "0.1",
    #"license_id": "unlicensed",
    "order": 0,
    "origin_id": "123",
    "origin_url": "www.domain.com",
    "origin_cms": "wordpress",
    "excerpt": "Test test 123",
    "global_slug": "0807 test",
    "imported_on": datetime.datetime.now(),
    "featured_media": {
    }
}
for key, value in CONTENT_TEMPLATE.items():
    if isinstance(value, (list, dict)):
        CONTENT_TEMPLATE[key] = json.dumps(value)


CHUNK_SIZE = 1500  # For bulk insert


class Command(BaseCommand):
    help = 'Generates content using orm'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--num-docs', nargs='?', type=str, default=0,
                            help='Number of content docs to generate')

    def handle(self, *args, **options):
        """
        Generate content docs! Insert 2.5m docs
        :param args:
        :param options:
        :return:
        """
        num_docs = int(options['num_docs'])

        # Slowest (get)
        # s = time.time()
        # [Content.objects.get_or_create(titles='{"main": "test tile", "seo": "test seo"}') for _ in range(num_docs)]
        # print("It took ", time.time() - s)

        # Slow
        # s = time.time()
        # [Content.objects.create(**CONTENT_TEMPLATE) for _ in range(num_docs)]
        # print("It took ", time.time() - s)

        # Fastest way
        # More or less size will be by full chunks
        chunks = int(math.ceil(num_docs/CHUNK_SIZE))

        # contents = [Content(**CONTENT_TEMPLATE) for _ in range(CHUNK_SIZE)]

        s = time.time()

        print("NUmber of chunks is ", chunks)
        for chunk in range(chunks):
            Content.objects.bulk_create([Content(**CONTENT_TEMPLATE) for _ in range(CHUNK_SIZE)])
            print("Done inserting chunk {} of {}, time {}".format(chunk, chunks, round(time.time() -s, 3)))

        print("It took ", time.time() - s)

        print("There are now ", Content.objects.count(), " Content objects")
