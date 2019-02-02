"""
Validate for json content
"""

from django.core.management.base import BaseCommand

from content_app.models import Content
from django.conf import settings

# from collections import OrderedDict
import pymongo


# djongo.base  get_connection_params
def get_connection_params(settings_dict):
    """
    Default method to acquire database connection parameters.

    Sets connection parameters to match settings.py, and sets
    default values to blank fields.
    """
    valid_settings = {
        'NAME': 'name',
        'HOST': 'host',
        'PORT': 'port',
        'USER': 'username',
        'PASSWORD': 'password',
        'AUTH_SOURCE': 'authSource',
        'AUTH_MECHANISM': 'authMechanism',
        'ENFORCE_SCHEMA': 'enforce_schema',
        'REPLICASET': 'replicaset',
        'SSL': 'ssl',
        'SSL_CERTFILE': 'ssl_certfile',
        'SSL_CA_CERTS': 'ssl_ca_certs',
        'READ_PREFERENCE': 'read_preference'
    }
    connection_params = {
        'name': 'djongo_test',
        'enforce_schema': True
    }
    for setting_name, kwarg in valid_settings.items():
        try:
            setting = settings_dict[setting_name]
        except KeyError:
            continue

        if setting or setting is False:
            connection_params[kwarg] = setting

    return connection_params

CHUNK_SIZE = 100

MONGO_SETTINGS = settings.DATABASES['mongo']

CONN_PARAMS = get_connection_params(MONGO_SETTINGS)
del CONN_PARAMS['enforce_schema']
del CONN_PARAMS['name']
# CONN_PARAMS['document_class'] = OrderedDict


JSON_FIELDS = []
for field in Content._meta.get_fields():
    if 'djongo.models.json.JSONField' in str(field.db_type):
        JSON_FIELDS.append(field.name)


class Command(BaseCommand):
    help = 'Validate content using orm'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--num-docs', nargs='?', type=str, default=0,
                            help='Number of content docs')

    def handle(self, *args, **options):
        """
        Generate content docs! Insert 2.5m docs
        :param args:
        :param options:
        :return:
        """
        num_docs = int(options['num_docs'])

        contents = Content.objects.all()[:num_docs]
        for content in contents:
            print(content._id)

        # for n in range(num_docs):
        #     contents = Content.objects.all()[n:1]
        #     print(n, content._id)

        # One at a time
        # content = Content.objects.all()[0:1]
        # for c in content:
        #     print(c._id)

        # Pymongo way
        # client = pymongo.MongoClient(**CONN_PARAMS)
        # db = client[MONGO_SETTINGS['NAME']]
        # collection = db['content']
        # for n in range(num_docs):
        #     doc = collection.find_one()
        #     for f in JSON_FIELDS:
        #         print(f, doc[f], type(doc[f]))
        #         if not isinstance(doc[f], (list, dict)):
        #             raise Exception("No bueno")
