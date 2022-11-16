# Elastick packages
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer, char_filter
from django_elasticsearch_dsl.registries import registry
# Local apps
from .models import Product


html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    filter=["lowecase", "stop", "snowball"],
    char_filter=['html_strip']
)


@registry.register_document
class ProductDocument(Document):
    description = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )

    class Index:
        name = 'product'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Product
        fields = ['name']
